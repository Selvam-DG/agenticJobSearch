
from pathlib import Path

from fastapi import (
    Depends,
    FastAPI,
    Request,
)

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy import text
from sqlalchemy.orm import Session

from jobscout.api.profile import (
    router as profile_router,
)

from jobscout.core.security import require_admin
from jobscout.database.session import get_db


import os


ROOT = Path(
    os.environ.get("JOBSCOUT_ROOT", os.getcwd())
).resolve()

app = FastAPI(
    title="JobScout AI",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.include_router(profile_router)

app.mount(
    "/static",
    StaticFiles(
        directory=ROOT / "static"
    ),
    name="static",
)

templates = Jinja2Templates(
    directory=ROOT / "templates"
)


@app.get("/health/live")
def live():
    return {
        "status": "ok",
        "version": "0.1.0",
    }


@app.get("/health/ready")
def ready(
    _: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    db.execute(
        text("SELECT 1")
    )

    return {
        "status": "ready",
        "database": "ok",
    }


@app.get(
    "/",
    response_class=HTMLResponse,
)
def dashboard(
    request: Request,
    _: str = Depends(require_admin),
):
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "version": "0.1.0"
        },
    )
