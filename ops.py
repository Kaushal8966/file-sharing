from fastapi import APIRouter, UploadFile, File, HTTPException, Header, Depends
from app.auth import decode_token
from app.database import db
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Allowed file types for Ops upload
ALLOWED_TYPES = [
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",    # .docx
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",          # .xlsx
    "application/vnd.openxmlformats-officedocument.presentationml.presentation"   # .pptx
]

# Helper to get user from JWT
def get_current_user(token: str = Header(...)):
    return decode_token(token)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), user=Depends(get_current_user)):
    if user["role"] != "ops":
        raise HTTPException(status_code=403, detail="Only Ops users can upload files.")

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type.")

    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    await db.files.insert_one({
        "filename": file.filename,
        "uploaded_by": user["user_id"]
    })

    return {"message": "File uploaded successfully."}
