
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from jobscout.database.models import (
    ProfileSkill,
    TargetLocation,
    TargetRole,
    UserProfile,
)

from jobscout.schemas.profile import (
    ProfileIn,
    ProfileOut,
)


def load_profile(
    db: Session,
) -> UserProfile | None:
    return db.scalar(
        select(UserProfile)
        .where(UserProfile.id == 1)
        .options(
            selectinload(UserProfile.skills),
            selectinload(UserProfile.roles),
            selectinload(UserProfile.locations),
        )
    )


def serialize_profile(
    profile: UserProfile | None,
) -> ProfileOut:
    if profile is None:
        return ProfileOut()

    return ProfileOut(
        display_name=profile.display_name,
        current_location=profile.current_location,
        years_experience=profile.years_experience,
        work_mode=profile.work_mode,
        skills=[
            {
                "name": s.name,
                "proficiency": s.proficiency,
            }
            for s in profile.skills
        ],
        roles=[
            r.name
            for r in profile.roles
        ],
        locations=[
            {
                "city": l.city,
                "radius_km": l.radius_km,
            }
            for l in profile.locations
        ],
    )


def save_profile(
    db: Session,
    data: ProfileIn,
) -> ProfileOut:
    profile = load_profile(db)

    if profile is None:
        profile = UserProfile(id=1)
        db.add(profile)

    profile.display_name = data.display_name.strip()
    profile.current_location = (
        data.current_location.strip()
    )
    profile.years_experience = data.years_experience
    profile.work_mode = data.work_mode

    profile.skills = [
        ProfileSkill(
            name=s.name.strip(),
            proficiency=s.proficiency,
        )
        for s in data.skills
    ]

    profile.roles = [
        TargetRole(name=r.strip())
        for r in data.roles
    ]

    profile.locations = [
        TargetLocation(
            city=l.city.strip(),
            radius_km=l.radius_km,
        )
        for l in data.locations
    ]

    db.commit()

    return serialize_profile(
        load_profile(db)
    )
