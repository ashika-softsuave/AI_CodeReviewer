#Main
from fastapi import FastAPI
from routes.route import router as agentic_router

app = FastAPI()
app.include_router(agentic_router)
