# In app/routes/client.py

from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/client/display/{filename}")
async def display_file(filename: str):
    file_path = f"uploads/{filename}"  # Adjust this to your actual upload path
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"detail": "File not found"}
