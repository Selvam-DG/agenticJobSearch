
import pytest

from pydantic import ValidationError

from jobscout.schemas.profile import ProfileIn


def test_valid_profile():
    profile = ProfileIn.model_validate({
        "display_name": "A Candidate",
        "roles": [
            "Python Developer",
            "Backend Developer",
        ],
        "skills": [
            {
                "name": "Python",
                "proficiency": "advanced",
            }
        ],
        "locations": [
            {
                "city": "Munich",
                "radius_km": 30,
            }
        ],
        "work_mode": "hybrid",
    })

    assert profile.skills[0].name == "Python"


@pytest.mark.parametrize(
    "payload",
    [
        {
            "skills": [
                {"name": "Python"},
                {"name": "python"},
            ]
        },
        {
            "roles": [
                "Backend",
                "backend",
            ]
        },
        {
            "roles": ["  "]
        },
        {
            "locations": [
                {
                    "city": "Munich",
                    "radius_km": 0,
                }
            ]
        },
        {
            "work_mode": "spaceship"
        },
        {
            "years_experience": -1
        },
    ],
)
def test_invalid_profiles(payload):
    with pytest.raises(ValidationError):
        ProfileIn.model_validate(payload)