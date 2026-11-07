
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    display_name: Mapped[str] = mapped_column(
        String(120),
        default="",
    )

    current_location: Mapped[str] = mapped_column(
        String(160),
        default="",
    )

    years_experience: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    work_mode: Mapped[str] = mapped_column(
        String(12),
        default="any",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    skills: Mapped[list["ProfileSkill"]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        order_by="ProfileSkill.id",
    )

    roles: Mapped[list["TargetRole"]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        order_by="TargetRole.id",
    )

    locations: Mapped[list["TargetLocation"]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        order_by="TargetLocation.id",
    )


class ProfileSkill(Base):
    __tablename__ = "profile_skills"

    __table_args__ = (
        UniqueConstraint(
            "profile_id",
            "name",
            name="uq_profile_skill",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    profile_id: Mapped[int] = mapped_column(
        ForeignKey(
            "user_profiles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    proficiency: Mapped[str] = mapped_column(
        String(20),
        default="intermediate",
    )

    profile: Mapped[UserProfile] = relationship(
        back_populates="skills",
    )


class TargetRole(Base):
    __tablename__ = "target_roles"

    __table_args__ = (
        UniqueConstraint(
            "profile_id",
            "name",
            name="uq_profile_role",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    profile_id: Mapped[int] = mapped_column(
        ForeignKey(
            "user_profiles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    profile: Mapped[UserProfile] = relationship(
        back_populates="roles",
    )


class TargetLocation(Base):
    __tablename__ = "target_locations"

    __table_args__ = (
        UniqueConstraint(
            "profile_id",
            "city",
            name="uq_profile_location",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    profile_id: Mapped[int] = mapped_column(
        ForeignKey(
            "user_profiles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    city: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    radius_km: Mapped[int] = mapped_column(
        Integer,
        default=30,
    )

    profile: Mapped[UserProfile] = relationship(
        back_populates="locations",
    )
