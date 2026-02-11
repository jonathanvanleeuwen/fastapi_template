import logging
from datetime import UTC, datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer

from {{cookiecutter.project_name}}.settings import get_settings

logger = logging.getLogger(__name__)


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="/auth/oauth/authorize",
    tokenUrl="/auth/oauth/token",
    auto_error=False,
)

# Module-level singleton to satisfy B008 linter rule
_depends_oauth2_scheme = Depends(oauth2_scheme)


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
    roles: list[str] | None = None,
) -> str:
    settings = get_settings()
    to_encode = data.copy()

    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.oauth_access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})

    if roles:
        to_encode["roles"] = roles

    return jwt.encode(to_encode, settings.oauth_secret_key, algorithm="HS256")


def verify_access_token(token: str) -> dict[str, Any]:
    settings = get_settings()
    payload = jwt.decode(
        token,
        settings.oauth_secret_key,
        algorithms=["HS256"],
        options={"verify_exp": False},
    )
    token_exp = payload.get("exp", 0)
    exp_utc = datetime.fromtimestamp(token_exp, tz=timezone.utc) if token_exp > 0 else None
    logger.debug(
        "Token payload after decoding (without verifying expiration): %s",
        payload,
        extra=payload,
    )
    logger.debug("Token expiration time [UTC]: %s", exp_utc, extra={"exp": token_exp, "exp_utc": exp_utc})
    try:
        payload = jwt.decode(token, settings.oauth_secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        ) from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from exc
