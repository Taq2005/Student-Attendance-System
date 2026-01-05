import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import cv2

from attendance import attendance
import threading
import webbrowser
import serviceAcc as sc
from Supabase_client import supabase
# ================= CONFIG =================
ADMIN_PASSWORD = "admin123"
MAX_ATTEMPTS = 3
attempts = 0

# ================= THREAD LAUNCHER =================
def launch_attendance():
    threading.Thread(target=attendance, daemon=True).start()
#to open supabase online
def view_database():
    webbrowser.open(sc.Table_url)
def get_student_ids():
    try:
        response = supabase.table("Students").select("id").execute()
        return [str(row["id"]) for row in response.data]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch IDs\n{e}")
        return []

#Edit database
def edit_database():
    clear_content()

    tk.Label(
        content,
        text="Edit Student Record",
        font=("Segoe UI", 16, "bold"),
        bg="#ffffff"
    ).pack(pady=20)

    body = tk.Frame(content, bg="#ffffff")
    body.pack(pady=20)

    # ---------------- ID DROPDOWN ----------------
    tk.Label(body, text="Student ID", bg="#ffffff", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w", pady=5)

    student_ids = get_student_ids()
    selected_id = tk.StringVar()

    id_dropdown = ttk.Combobox(
        body,
        textvariable=selected_id,
        values=student_ids,
        state="readonly",
        width=25
    )
    id_dropdown.grid(row=0, column=1, pady=5)

    # ---------------- COLUMN DROPDOWN ----------------
    tk.Label(body, text="Select Column", bg="#ffffff", font=("Segoe UI", 11)).grid(row=1, column=0, sticky="w", pady=5)

    columns = [
        "Name",
        "Major",
        "year",
        "standing",
        "starting_year",
        "total_attendance",
        "last_attendance"
    ]

    selected_column = tk.StringVar()

    column_dropdown = ttk.Combobox(
        body,
        textvariable=selected_column,
        values=columns,
        state="readonly",
        width=25
    )
    column_dropdown.grid(row=1, column=1, pady=5)

    # ---------------- NEW VALUE ----------------
    tk.Label(body, text="Change To", bg="#ffffff", font=("Segoe UI", 11)).grid(row=2, column=0, sticky="w", pady=5)

    new_value = tk.Entry(body, width=28, font=("Segoe UI", 11))
    new_value.grid(row=2, column=1, pady=5)

    # ---------------- BUTTONS ----------------
    btn_frame = tk.Frame(content, bg="#ffffff")
    btn_frame.pack(pady=30)

    def update_record():
        if not selected_id.get() or not selected_column.get() or not new_value.get():
            messagebox.showwarning("Missing Data", "Please fill all fields")
            return
        column = selected_column.get()
        value = new_value.get()
        if selected_column == "last_attendance":
            from datetime import datetime
            value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S").isoformat()

        try:
            supabase.table("Students") \
                .update({column:value}) \
                .eq("id", selected_id.get()) \
                .execute()

            messagebox.showinfo("Success", "Record updated successfully")
            new_value.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Update Failed", str(e))

    ttk.Button(
        btn_frame,
        text="Update",
        style="Modern.TButton",
        width=16,
        command=update_record
    ).grid(row=0, column=0, padx=15)

    ttk.Button(
        btn_frame,
        text="Back",
        style="Modern.TButton",
        width=16,
        command=open_admin_panel
    ).grid(row=0, column=1, padx=15)
def add_student():
    clear_content()

    tk.Label(
        content,
        text="Add Student Record",
        font=("Segoe UI", 16, "bold"),
        bg="#ffffff"
    ).pack(pady=10)

    body = tk.Frame(content, bg="#ffffff")
    body.pack(pady=10)

    # -------- FORM FIELDS --------
    fields = {
        "Name": tk.StringVar(),
        "ID": tk.StringVar(),
        "Major": tk.StringVar(),
        "Starting Year": tk.StringVar(),
        "Current Year": tk.StringVar()
    }

    for i, (label, var) in enumerate(fields.items()):
        tk.Label(body, text=label, bg="#ffffff", font=("Segoe UI", 11)) \
            .grid(row=i, column=0, sticky="w", pady=5)
        tk.Entry(body, textvariable=var, width=28) \
            .grid(row=i, column=1, pady=5)

    # -------- IMAGE UPLOAD --------
    image_path = tk.StringVar()

    def upload_image():
        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
        )
        if not path:
            return

        img = cv2.imread(path)
        h, w, _ = img.shape

        if h != w:
            messagebox.showerror("Invalid Image", "Image must be square (1:1)")
            return

        image_path.set(path)
        messagebox.showinfo("Image Selected", "Image uploaded successfully")

    tk.Label(body, text="Upload Photo (Square Only)", bg="#ffffff") \
        .grid(row=6, column=0, sticky="w", pady=5)

    tk.Button(body, text="Choose Image", command=upload_image) \
        .grid(row=6, column=1, pady=5)

    # -------- SUBMIT --------
    def submit_student():
        if not all(v.get() for v in fields.values()) or not image_path.get():
            messagebox.showwarning("Missing Data", "Please fill all fields")
            return

        try:
            img = cv2.imread(image_path.get())
            img = cv2.resize(img, (128, 128))
            _, buffer = cv2.imencode(".jpg", img)

            student_id = fields["ID"].get()

            supabase.storage.from_("Images").upload(
                f"{student_id}.jpg",
                buffer.tobytes(),
                {"content-type": "image/jpeg"}
            )

            supabase.table("Students").insert({
                "id": student_id,
                "Name": fields["Name"].get(),
                "Major": fields["Major"].get(),
                "starting_year": int(fields["Starting Year"].get()),
                "year": int(fields["Current Year"].get()),
                "total_attendance": 0,
                "last_attendance": None,
                "standing": "G"
            }).execute()

            messagebox.showinfo("Success", "Student added successfully")
            open_admin_panel()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # -------- BUTTONS (INSIDE BODY) --------
    btn_frame = tk.Frame(body, bg="#ffffff")
    btn_frame.grid(row=7, column=0, columnspan=2, pady=20)

    ttk.Button(
        btn_frame,
        text="Add",
        style="Modern.TButton",
        width=16,
        command=submit_student
    ).grid(row=0, column=0, padx=10)

    ttk.Button(
        btn_frame,
        text="Back",
        style="Modern.TButton",
        width=16,
        command=open_admin_panel
    ).grid(row=0, column=1, padx=10)


# ADMIN PANEL
def open_admin_panel():
    clear_content()
    tk.Label(
        content,
        text="Admin Panel",
        font=("Segoe UI", 16, "bold"),
        bg="#ffffff"
    ).pack(pady=20)

    body = tk.Frame(content, bg="#ffffff")
    body.pack(expand=True)

    btn_style = {
        "font": ("Segoe UI", 12),
        "width": 18,
        "height": 2
    }

    # 2 x 2 layout
    tk.Button(body, text="Add Student",**btn_style, command = add_student).grid(row=0, column=0, padx=20, pady=20)
    tk.Button(body, text="View Database", **btn_style,command = view_database).grid(row=0, column=1, padx=20, pady=20)
    tk.Button(body, text="Edit Database", **btn_style, command = edit_database).grid(row=1, column=0, padx=20, pady=20)
    tk.Button(body, text="Exit", **btn_style, command=show_home).grid(row=1, column=1, padx=20, pady=20)

# ================= PASSWORD PROMPT =================
def admin_login():

    clear_content()
    global attempts

    if attempts >= MAX_ATTEMPTS:
        messagebox.showerror("Access Denied", "Too many incorrect attempts!")
        return

    tk.Label(
        content,
        text="Admin Login",
        font=("Segoe UI", 16, "bold"),
        bg="#ffffff"
    ).pack(pady=20)

    password_entry = tk.Entry(content, show="*", font=("Segoe UI", 12), width=22)
    password_entry.pack(pady=10)
    password_entry.focus()

    password_entry.bind("<Return>", lambda e: verify())

    def verify():
        global attempts
        if password_entry.get() == ADMIN_PASSWORD:
            attempts = 0
            clear_content()
            open_admin_panel()
        else:
            attempts += 1
            remaining = MAX_ATTEMPTS - attempts
            if remaining > 0:
                messagebox.showerror("Incorrect", f"Wrong password! Attempts left: {remaining}")
            else:
                messagebox.showerror("Locked", "Too many incorrect attempts!")
                clear_content()
                show_home()

    tk.Button(
        content,
        text="Login",
        font=("Segoe UI", 11),
        width=12,
        command=verify
    ).pack(pady=15)
def show_home():
    clear_content()

    tk.Label(
        content,
        text="Choose an option",
        font=("Segoe UI", 14),
        bg="#ffffff",
        fg="#555"
    ).pack(pady=30)

    btn_frame = tk.Frame(content, bg="#ffffff")
    btn_frame.pack()

    ttk.Button(
        btn_frame,
        text="Admin Panel",
        style="Modern.TButton",
        width=22,
        command=admin_login
    ).grid(row=0, column=0, padx=20)

    ttk.Button(
        btn_frame,
        text="Student Attendance",
        style="Modern.TButton",
        width=22,
        command=launch_attendance
    ).grid(row=0, column=1, padx=20)


def clear_content():
    for widget in content.winfo_children():
        widget.destroy()

root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("800x500")
root.configure(bg="#ffffff")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Modern.TButton",
    font=("Segoe UI", 13),
    padding=12,
    background="#6D5DF6",
    foreground="white"
)

style.map("Modern.TButton", background=[("active", "#1e40af")])

header = tk.Frame(root, bg="#6D5DF6", height=90)
header.pack(fill="x")
tk.Label(
    header,
    text="Face Recognition Attendance System",
    font=("Segoe UI", 22, "bold"),
    bg="#6D5DF6",
    fg="white"
).pack(pady=25)
tk.Label(
        root,
        text="© 2025 Attendance System",
        font=("Segoe UI", 9),
        bg="#ffffff",
        fg="#999"
    ).pack(side="bottom", pady=10)
content = tk.Frame(root, bg="#ffffff")
content.pack(expand = True, fill="both")
show_home()
root.mainloop()
