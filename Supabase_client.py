import numpy as np
import cv2
import serviceAcc
from supabase import create_client
URL = serviceAcc.Project_url
Key = serviceAcc.Project_api

supabase = create_client(URL, Key)


