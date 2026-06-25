from pathlib import Path

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from src.database.db import get_analysis_by_id

from src.pipeline.analyze_uploaded_contract import (
    analyze_contract
)

from src.database.db import (
    save_analysis,
    get_all_analyses
)

router = APIRouter()

UPLOAD_DIR = Path(
    "data/uploads"
)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


@router.post("/analyze")
async def analyze_pdf(
    file: UploadFile = File(...)
):

    file_path = (
        UPLOAD_DIR /
        file.filename
    )

    contents = await file.read()

    with open(
        file_path,
        "wb"
    ) as f:

        f.write(contents)

    result = analyze_contract(
        file_path
    )

    save_analysis(
        filename=file.filename,
        contract_type=result.get(
            "contract_type"
        ),
        risk_score=result.get(
            "risk_score"
        ),
        risk_level=result.get(
            "risk_level"
        ),
        summary = result.get(
            "summary"
        ),
        analysis_json=result       
    )

    return result


@router.get("/history")
def history():

    return get_all_analyses()

@router.get("/history/{analysis_id}")
def get_analysis(
    analysis_id: int
):

    return get_analysis_by_id(
        analysis_id
    )
