from fastapi import APIRouter
from pydantic import BaseModel
from services.agentic_service import run_agentic_fix

router = APIRouter()

class CommandRequest(BaseModel):
    instruction: str

#Endpoint
@router.post("/agentic-fix-file")
def agentic_fix_file(req: CommandRequest):
    return run_agentic_fix(req.instruction)
