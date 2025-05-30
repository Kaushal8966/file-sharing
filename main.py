from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Routes go here
@app.get("/", response_class=HTMLResponse)
def home():
    return "<h1>Welcome to Secure File Sharing</h1>"

# Example upload route
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    upload_dir = os.path.join(os.path.dirname(__file__), "..", "uploaded_files")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}

# ⬇️ Put this at the **bottom of your file**
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

