from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

router = APIRouter()

@router.post("/analyze")
async def analyze_contract(
    file: UploadFile = File(...)
):

    return {
        "filename": file.filename,
        "message": "File received successfully"
    }

