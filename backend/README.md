# InfoFi Backend

FastAPI-based backend for the InfoFi intelligence platform.

## Quick Start

### 1. Setup Environment

```bash
# Copy environment file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Database Migrations

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Run migration
alembic upgrade head
```

### 4. Run the Application

```bash
# Development mode
uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker Compose

Run the entire stack with Docker:

```bash
# From project root
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

## Project Structure

```
backend/
├── app/
│   ├── api/v1/         # API endpoints
│   ├── core/           # Security, caching, etc.
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic
│   ├── tasks/          # Celery tasks
│   ├── db/             # Database config
│   ├── utils/          # Utilities
│   ├── config.py       # Settings
│   └── main.py         # FastAPI app
├── tests/              # Tests
├── scripts/            # Utility scripts
├── requirements.txt
└── Dockerfile
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Email/password login
- `POST /api/v1/auth/wallet-login` - Web3 wallet login
- `GET /api/v1/auth/me` - Get current user

### Platforms
- `GET /api/v1/platforms` - List platforms
- `GET /api/v1/platforms/{id}` - Get platform details

### Campaigns
- `GET /api/v1/campaigns` - List campaigns (with filters)
- `GET /api/v1/campaigns/{id}` - Get campaign details

### Profiles
- `GET /api/v1/profiles/me` - Get my platform profiles

### Analytics
- `GET /api/v1/analytics/dashboard-stats` - Dashboard statistics
- `GET /api/v1/analytics/leaderboard/global` - Global leaderboard

## Development

### Run Tests

```bash
pytest
```

### Format Code

```bash
black app/
flake8 app/
```

### Create Database Migration

```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `SECRET_KEY` - JWT secret key
- `OLLAMA_HOST` - Ollama LLM service URL

