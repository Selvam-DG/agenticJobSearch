
const fieldNames = [
  "display_name",
  "current_location",
  "years_experience",
  "work_mode",
  "roles",
  "skills",
  "locations"
];

const fields = Object.fromEntries(
  fieldNames.map(name => [
    name,
    document.getElementById(name)
  ])
);

const message = document.getElementById("message");


function lines(value) {
  return value
    .split("\n")
    .map(item => item.trim())
    .filter(Boolean);
}


function render(profile) {
  fields.display_name.value =
    profile.display_name;

  fields.current_location.value =
    profile.current_location;

  fields.years_experience.value =
    profile.years_experience;

  fields.work_mode.value =
    profile.work_mode;

  fields.roles.value =
    profile.roles.join("\n");

  fields.skills.value =
    profile.skills
      .map(skill =>
        `${skill.name} | ${skill.proficiency}`
      )
      .join("\n");

  fields.locations.value =
    profile.locations
      .map(location =>
        `${location.city} | ${location.radius_km}`
      )
      .join("\n");
}


function payload() {
  return {
    display_name:
      fields.display_name.value.trim(),

    current_location:
      fields.current_location.value.trim(),

    years_experience:
      Number(fields.years_experience.value),

    work_mode:
      fields.work_mode.value,

    roles:
      lines(fields.roles.value),

    skills:
      lines(fields.skills.value).map(item => {
        const [
          name,
          proficiency = "intermediate"
        ] = item
          .split("|")
          .map(value => value.trim());

        return {
          name,
          proficiency
        };
      }),

    locations:
      lines(fields.locations.value).map(item => {
        const [
          city,
          radius = "30"
        ] = item
          .split("|")
          .map(value => value.trim());

        return {
          city,
          radius_km: Number(radius)
        };
      })
  };
}


async function load() {
  try {
    const response = await fetch(
      "/api/v1/profile"
    );

    if (!response.ok) {
      throw new Error(
        `Unable to load profile (${response.status})`
      );
    }

    const data = await response.json();
    render(data);

  } catch (error) {
    message.textContent = error.message;
  }
}


document
  .getElementById("profile-form")
  .addEventListener("submit", async event => {

    event.preventDefault();

    message.textContent = "Saving...";

    try {
      const response = await fetch(
        "/api/v1/profile",
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(payload())
        }
      );

      if (!response.ok) {
        const error = await response.json();

        throw new Error(
          `Save failed: ${JSON.stringify(error.detail)}`
        );
      }

      const data = await response.json();

      render(data);

      message.textContent =
        "Profile saved successfully.";

    } catch (error) {
      message.textContent = error.message;
    }
  });


load();
