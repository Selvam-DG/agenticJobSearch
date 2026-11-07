
# JobScout AI Architecture

## Version 0.1.0

The application uses one FastAPI service with
an external PostgreSQL database.

## Request flow

Browser
  -> FastAPI
  -> Pydantic validation
  -> Profile service
  -> SQLAlchemy
  -> PostgreSQL

## Components

### API
Handles incoming HTTP requests.

### Schemas
Validates request and response data.

### Services
Implements business logic.

### Database
Stores persistent profile information.

### Templates and static files
Provides the user dashboard.

## Future architecture

- Job source connectors
- Scheduled monitoring
- Ollama inference
- LangGraph orchestration
- Email notifications
- Application tracking
