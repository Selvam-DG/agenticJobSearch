
import secrets

from fastapi import (
    Depends,
    HTTPException,
    status,
)

from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials,
)

from jobscout.core.config import (
    Settings,
    get_settings,
)


basic_auth = HTTPBasic()


def require_admin(
    credentials: HTTPBasicCredentials = Depends(
        basic_auth
    ),
    settings: Settings = Depends(get_settings),
) -> str:

    username_ok = secrets.compare_digest(
        credentials.username.encode(),
        settings.admin_username.encode(),
    )

    password_ok = secrets.compare_digest(
        credentials.password.encode(),
        settings.admin_password.encode(),
    )

    if not (username_ok and password_ok):
        raise HTTPException(
            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),
            detail="Invalid credentials",
            headers={
                "WWW-Authenticate": "Basic"
            },
        )

    return credentials.username
