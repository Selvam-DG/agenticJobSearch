
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from jobscout.core.security import require_admin
from jobscout.database.session import get_db

from jobscout.schemas.profile import (
    ProfileIn,
    ProfileOut,
)

from jobscout.services.profile import (
    load_profile,
    save_profile,
    serialize_profile,
)


router = APIRouter(
    prefix="/api/v1/profile",
    tags=["profile"],
    dependencies=[Depends(require_admin)],
)


@router.get(
    "",
    response_model=ProfileOut,
)
def get_profile(
    db: Session = Depends(get_db),
):
    return serialize_profile(
        load_profile(db)
    )


@router.put(
    "",
    response_model=ProfileOut,
)
def put_profile(
    payload: ProfileIn,
    db: Session = Depends(get_db),
):
    return save_profile(
        db,
        payload,
    )
