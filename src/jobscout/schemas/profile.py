
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class SkillIn(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )

    proficiency: Literal[
        "beginner",
        "intermediate",
        "advanced",
        "expert",
    ] = "intermediate"


class LocationIn(BaseModel):
    city: str = Field(
        min_length=1,
        max_length=120,
    )

    radius_km: int = Field(
        default=30,
        ge=1,
        le=500,
    )


class ProfileIn(BaseModel):
    display_name: str = Field(
        default="",
        max_length=120,
    )

    current_location: str = Field(
        default="",
        max_length=160,
    )

    years_experience: int = Field(
        default=0,
        ge=0,
        le=60,
    )

    work_mode: Literal[
        "any",
        "remote",
        "hybrid",
        "onsite",
    ] = "any"

    skills: list[SkillIn] = Field(
        default_factory=list,
        max_length=100,
    )

    roles: list[str] = Field(
        default_factory=list,
        max_length=40,
    )

    locations: list[LocationIn] = Field(
        default_factory=list,
        max_length=40,
    )

    @field_validator("roles")
    @classmethod
    def valid_roles(
        cls,
        roles: list[str],
    ) -> list[str]:
        if any(
            not name.strip() or len(name) > 120
            for name in roles
        ):
            raise ValueError(
                "Roles must be nonempty and "
                "at most 120 characters"
            )
        return roles

    @field_validator("skills")
    @classmethod
    def unique_skills(
        cls,
        skills: list[SkillIn],
    ) -> list[SkillIn]:
        names = {
            s.name.strip().casefold()
            for s in skills
        }

        if len(names) != len(skills):
            raise ValueError(
                "Duplicate skill names"
            )

        return skills

    @field_validator("roles")
    @classmethod
    def unique_roles(
        cls,
        roles: list[str],
    ) -> list[str]:
        names = {
            r.strip().casefold()
            for r in roles
        }

        if len(names) != len(roles):
            raise ValueError(
                "Duplicate roles"
            )

        return roles

    @field_validator("locations")
    @classmethod
    def unique_locations(
        cls,
        locations: list[LocationIn],
    ) -> list[LocationIn]:
        names = {
            l.city.strip().casefold()
            for l in locations
        }

        if len(names) != len(locations):
            raise ValueError(
                "Duplicate locations"
            )

        return locations


class ProfileOut(ProfileIn):
    model_config = ConfigDict(
        from_attributes=True,
    )
