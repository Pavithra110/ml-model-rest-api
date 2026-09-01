from fastapi import FastAPI
import joblib
import uuid
from contextlib import asynccontextmanager
from app.logging_config import logger
from app.routers.v1 import router as v1_router
from app.config import settings
import time


@asynccontextmanager
async def lifespan(app):
    app.state.model = joblib.load(settings.MODEL_PATH)
    logger.info("ML model loaded successfully")
    yield


app = FastAPI(
    title=settings.API_TITLE,
    lifespan=lifespan
)
app.include_router(v1_router)


@app.middleware("http")
async def log_requests(request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        f"request_id={request_id} method={request.method} "
        f"path={request.url.path} duration={duration:.4f}s"
    )

    return response


@app.get("/")
def root():
    return {"message": "ML API is alive"}

