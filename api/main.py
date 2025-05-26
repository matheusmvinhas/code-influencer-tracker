from fastapi import FastAPI
from api.routes import all_routes
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import traceback

app = FastAPI()

@app.exception_handler(Exception)
async def all_exceptions_handler(request: Request, exc: Exception):
    print("=== ERRO GLOBAL ===")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )

app.include_router(all_routes.router)  # Isso importa todas as rotas de uma vez

@app.get("/")
def root():
    return {"message": "Influencer API is running 🚀"}