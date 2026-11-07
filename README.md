# agenticJobSearch

**A self-hosted agentic AI job discovery, monitoring, and application tracking platform.**

agenticJobSearch is an open-source Python application designed to automate job discovery, monitor supported job platforms, match opportunities against user skills, and track job applications.

Built with **FastAPI, PostgreSQL, Docker, Ollama, and LangGraph**, the platform follows an incremental development approach, starting with a single-user application and evolving toward a multi-user AI-agent system.

**Current version:** `v0.1.0 — Backend & Profile Foundation`

>
> Job discovery, AI matching, LangGraph orchestration, and notifications are planned features. They are not implemented in this release.

## Features

### Available in v0.1.0

- FastAPI-based application backend
- Responsive dashboard using Jinja2, HTML, CSS, and JavaScript
- Single-administrator authentication using HTTP Basic
- Persistent job-search profile management
- Target job roles and preferred work locations
- Skills and proficiency levels
- Geographic search radius
- Work-mode preferences (remote, hybrid, on-site)
- SQLAlchemy ORM with PostgreSQL
- Alembic database migrations
- Docker Compose deployment
- Application health endpoints
- Automated tests and GitHub Actions CI

### Planned Features

- Automated job discovery from permitted sources
- Company career-page monitoring
- Job deduplication and publication tracking
- Scheduled job searches
- Ollama-based AI job analysis
- LangGraph multi-agent orchestration
- Skills-based suitability scoring
- Email and push notifications
- Application status tracking
- Multi-user account support

## Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12+ |
| Backend | FastAPI |
| Frontend | Jinja2, HTML5, CSS3, JavaScript |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.x |
| Migrations | Alembic |
| Validation | Pydantic |
| Deployment | Docker & Docker Compose |
| Testing | Pytest |
| Linting | Ruff |
| CI/CD | GitHub Actions |
| AI Integration (planned) | Ollama, Qwen |
| Agent Orchestration (planned) | LangGraph |

## Architecture

JobScout AI v0.1.0 runs as a single application service connected to an existing PostgreSQL instance.

```text
                   Web Browser
                       |
                       v
              FastAPI Application
                       |
            +----------+----------+
            |                     |
            v                     v
       Jinja2 Dashboard       REST API
                                  |
                                  v
                          Pydantic Validation
                                  |
                                  v
                            Service Layer
                                  |
                                  v
                             SQLAlchemy
                                  |
                                  v
                         External PostgreSQL
```

**Design principles**

- One application container for the initial deployment
- Business logic separated from API routes
- Database schema managed using migrations
- Credentials supplied through environment variables
- AI integrations added without replacing the backend architecture
- External PostgreSQL and Ollama services reused rather than duplicated

For more details, see [Architecture Documentation](docs/ARCHITECTURE.md).

## Project Structure

```text
jobscout-ai/
├── .github/
│   └── workflows/
├── alembic/
│   └── versions/
├── docs/
│   ├── AGENTS.md
│   ├── API.md
│   ├── ARCHITECTURE.md
│   ├── CONNECTORS.md
│   ├── DATABASE.md
│   ├── ROADMAP.md
│   └── SECURITY.md
├── setup/
│   └── check-services.sh
├── src/
│   └── jobscout/
│       ├── api/
│       ├── core/
│       ├── database/
│       ├── schemas/
│       ├── services/
│       └── main.py
├── static/
│   ├── css/
│   └── js/
├── templates/
├── tests/
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── compose.yaml
├── pyproject.toml
├── alembic.ini
├── Makefile
├── README.md
├── CHANGELOG.md
└── LICENSE
```

## Prerequisites

Before running the project, ensure you have:

- Python 3.12 or newer for local development
- Git
- Docker Engine and Docker Compose for containerized deployment
- An accessible PostgreSQL server
- Valid PostgreSQL database credentials

**Existing infrastructure**

The project supports a PostgreSQL server hosted on a different machine and connected through Tailscale.

Ollama is planned for later versions but is not required to run v0.1.0.

## Environment Configuration

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/jobscout-ai.git
cd jobscout-ai
```

Create your environment file:

```bash
cp .env.example .env
```

Edit the configuration:

```bash
nano .env
```

Minimum required configuration:

```dotenv
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000

DATABASE_URL=postgresql+psycopg://USERNAME:PASSWORD@POSTGRES_HOST:5432/jobscout

ADMIN_USERNAME=admin
ADMIN_PASSWORD=REPLACE_WITH_A_STRONG_PASSWORD
```

The remaining environment variables in `.env.example` are reserved for future monitoring, AI and notification integrations.

**Security:** Never commit `.env`, database credentials, administrator passwords or API tokens.

## Local Development

Use this option when developing, debugging or testing the application directly on your computer.

### 1. Create a Python virtual environment

```bash
python3.12 -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

Install the application and development dependencies:

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

Editable installation allows source-code changes without reinstalling the package.

### 3. Configure PostgreSQL

Verify that your `.env` file contains a valid `DATABASE_URL`.

The application requires an existing PostgreSQL database. It does not automatically create a database server.

### 4. Apply database migrations

```bash
alembic upgrade head
```

Verify the current database migration:

```bash
alembic current
```

### 5. Start the development server

```bash
uvicorn jobscout.main:app --reload --host 127.0.0.1 --port 8000
```

Alternatively, use the Makefile:

```bash
make run
```

Open:

**http://127.0.0.1:8000**

The application prompts for the administrator credentials configured in `.env`.

The `--reload` option automatically restarts the development server when Python source files change.

## Docker Deployment

Docker Compose is the recommended option for running the application on an Ubuntu server.

### 1. Build the image

```bash
docker compose build
```

### 2. Apply migrations

```bash
docker compose run --rm jobscout alembic upgrade head
```

### 3. Start the application

```bash
docker compose up -d
```

### 4. Verify container status

```bash
docker compose ps
```

### 5. View application logs

```bash
docker compose logs -f jobscout
```

### 6. Stop the application

```bash
docker compose down
```

PostgreSQL data is stored externally and is not removed by stopping the application container.

### Rebuilding after changes

```bash
docker compose up -d --build
```

If a new database migration is introduced, apply it before starting the updated application.

### Docker Networking

The application connects to PostgreSQL using the address configured in `DATABASE_URL`.

If PostgreSQL is hosted over Tailscale, verify that the Docker container can reach the remote host.

Do not use `localhost` for PostgreSQL unless it actually runs inside the same container.

The Compose configuration binds the application to:

```text
127.0.0.1:8000
```

For access from another machine, use an SSH tunnel or a properly secured reverse proxy over HTTPS.

## API Endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| GET | `/` | Administrator dashboard | Required |
| GET | `/health/live` | Application liveness | Public |
| GET | `/health/ready` | Database connectivity | Required |
| GET | `/api/v1/profile` | Retrieve job-search profile | Required |
| PUT | `/api/v1/profile` | Create or update profile | Required |

### Health Check

```bash
curl http://127.0.0.1:8000/health/live
```

Expected response:

```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

Check database readiness:

```bash
curl -u admin http://127.0.0.1:8000/health/ready
```

Enter the configured password when prompted.

### Retrieve Profile

```bash
curl -u admin http://127.0.0.1:8000/api/v1/profile
```

### Update Profile

```bash
curl -u admin -X PUT \
  http://127.0.0.1:8000/api/v1/profile \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "Developer",
    "current_location": "Munich, Germany",
    "years_experience": 3,
    "work_mode": "hybrid",
    "roles": [
      "Python Developer",
      "Backend Engineer",
      "AI Engineer"
    ],
    "skills": [
      {
        "name": "Python",
        "proficiency": "advanced"
      },
      {
        "name": "FastAPI",
        "proficiency": "intermediate"
      }
    ],
    "locations": [
      {
        "city": "Munich",
        "radius_km": 30
      }
    ]
  }'
```

## Testing and Code Quality

Run automated tests:

```bash
pytest -v
```

Run linting:

```bash
ruff check src tests --select E4,E7,E9,F
```

Check Python compilation:

```bash
python -m compileall -q src
```

Or use the Makefile:

```bash
make test
make lint
```

### PostgreSQL Integration Tests

Database integration tests must use a separate test database.

```bash
export TEST_DATABASE_URL="postgresql+psycopg://test_user:password@TEST_HOST:5432/jobscout_test"

pytest -q tests/test_postgres_integration.py
```

**Never configure the test database URL to point to your production database.** Integration tests may create, modify or remove test data.

## Database Migrations

Alembic manages database schema changes.

Apply pending migrations:

```bash
alembic upgrade head
```

Check database revision:

```bash
alembic current
```

Generate a proposed migration after changing SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe schema change"
```

Review generated migration code before applying it.

Migration files must be committed to Git so that the application and database schema remain versioned together.

## Troubleshooting

### Database connection failed

Verify that PostgreSQL is reachable, the credentials are correct, and the Tailscale network allows connectivity from the application container.

### Database tables are missing

Run:

```bash
docker compose run --rm jobscout alembic upgrade head
```

### Administrator authentication fails

Check `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `.env`. Restart the application after changing the environment configuration.

### Profile data disappears

Verify that the application and migration commands use the same PostgreSQL database.

### Ollama connection unavailable

Ollama is not required in version 0.1.0. AI inference will be introduced in a later milestone.

## Development Roadmap

| Version | Milestone |
|---|---|
| v0.1.0 | Backend, PostgreSQL and Profile Foundation |
| v0.2.0 | Job Collection and Persistence |
| v0.3.0 | Employer Career Monitoring |
| v0.4.0 | Scheduler and Notifications |
| v0.5.0 | Location-Based Company Discovery |
| v0.6.0 | Ollama and AI Search Planning |
| v0.7.0 | LangGraph Multi-Agent Orchestration |
| v0.8.0 | Intelligent Job Matching |
| v0.9.0 | Broader Job Source Coverage |
| v1.0.0 | Stable Personal Job Intelligence Platform |

Detailed planning is maintained in [ROADMAP.md](docs/ROADMAP.md).

## Security

JobScout AI v0.1.0 is designed for private, single-administrator use.

- Keep PostgreSQL credentials in environment variables.
- Use HTTPS for remote dashboard access.
- Keep database and Ollama endpoints off the public internet.
- Do not expose the administrator dashboard without authentication.
- Use a separate database for testing.
- Review migrations before applying them to production.
- Do not commit private CVs, API keys or personal information.

HTTP Basic authentication is a temporary solution for this early version. More robust session-based authentication and authorization are planned before enabling public account registration.

## Versioning

This project follows semantic versioning.

The initial foundation release is tagged:

`v0.1.0`

Development will continue through independently tested and documented milestones.

## License

See the [LICENSE](LICENSE) file for the project's licensing terms.

---

**AgenticJobSearch — Building an intelligent, self-hosted job discovery platform, one tested milestone at a time.**