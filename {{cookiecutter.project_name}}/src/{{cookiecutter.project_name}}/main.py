import logging
from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from lib_auth.auth.authentication import create_auth
from lib_auth.routers.oauth import create_oauth_router

from {{cookiecutter.project_name}}.custom_logger.setup.setup_logger import setup_logging
from {{cookiecutter.project_name}}.routers.math import math_router
from {{cookiecutter.project_name}}.settings import get_settings

settings = get_settings()
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version="1.0",
    description=settings.description,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for OAuth testing frontend (illustrative purposes only)
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount(
        "/static", StaticFiles(directory=str(static_dir), html=True), name="static"
    )


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/static/index.html")


# Add OAuth router from lib_auth
app.include_router(
    create_oauth_router(
        oauth_provider=settings.oauth_provider,
        oauth_client_id=settings.oauth_client_id,
        oauth_client_secret=settings.oauth_client_secret,
        oauth_secret_key=settings.oauth_secret_key,
        oauth_access_token_expire_minutes=settings.oauth_access_token_expire_minutes,
    )
)

# Add protected math router
app.include_router(
    math_router,
    dependencies=[
        Depends(
            create_auth(
                api_keys=settings.api_keys,
                oauth_secret_key=settings.oauth_secret_key,
                allowed_roles=["admin", "user"],
            )
        )
    ],
)
