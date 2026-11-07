
"""Initial profile tables."""

from alembic import op
import sqlalchemy as sa


revision = "0001_profile"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user_profiles",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),

        sa.Column(
            "display_name",
            sa.String(120),
            nullable=False,
        ),

        sa.Column(
            "current_location",
            sa.String(160),
            nullable=False,
        ),

        sa.Column(
            "years_experience",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "work_mode",
            sa.String(12),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_table(
        "profile_skills",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),

        sa.Column(
            "profile_id",
            sa.Integer(),
            sa.ForeignKey(
                "user_profiles.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),

        sa.Column(
            "name",
            sa.String(100),
            nullable=False,
        ),

        sa.Column(
            "proficiency",
            sa.String(20),
            nullable=False,
        ),

        sa.UniqueConstraint(
            "profile_id",
            "name",
            name="uq_profile_skill",
        ),
    )

    op.create_table(
        "target_roles",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),

        sa.Column(
            "profile_id",
            sa.Integer(),
            sa.ForeignKey(
                "user_profiles.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),

        sa.Column(
            "name",
            sa.String(120),
            nullable=False,
        ),

        sa.UniqueConstraint(
            "profile_id",
            "name",
            name="uq_profile_role",
        ),
    )

    op.create_table(
        "target_locations",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),

        sa.Column(
            "profile_id",
            sa.Integer(),
            sa.ForeignKey(
                "user_profiles.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),

        sa.Column(
            "city",
            sa.String(120),
            nullable=False,
        ),

        sa.Column(
            "radius_km",
            sa.Integer(),
            nullable=False,
        ),

        sa.UniqueConstraint(
            "profile_id",
            "city",
            name="uq_profile_location",
        ),
    )


def downgrade() -> None:
    op.drop_table("target_locations")
    op.drop_table("target_roles")
    op.drop_table("profile_skills")
    op.drop_table("user_profiles")
