from fastapi import FastAPI

from prometheus_fastapi_instrumentator import Instrumentator

from app.views import router


def start_app() -> FastAPI:
    app = FastAPI()

    app.include_router(router)

    Instrumentator().instrument(app).expose(app, include_in_schema=True)

    return app
