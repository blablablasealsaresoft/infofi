# 🚀 Getting Started with InfoFi

This guide will help you set up and run the InfoFi platform locally.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 20+** - [Download](https://nodejs.org/)
- **PostgreSQL 15+** - [Download](https://www.postgresql.org/download/)
- **Redis 7+** - [Download](https://redis.io/download/)
- **Ollama** - [Download](https://ollama.com/) (for AI features)
- **Docker** (optional, recommended) - [Download](https://www.docker.com/get-started/)

## 🐳 Quick Start with Docker (Recommended)

The easiest way to get started is using Docker Compose:

```bash
# 1. Pull the Ollama model
ollama pull deepseek-r1

# 2. Start all services
docker-compose up -d

# 3. Wait for services to be ready (check logs)
docker-compose logs -f api

# 4. Access the application
# Frontend: http://localhost:3000
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

That's it! The platform is now running.

## 💻 Manual Setup (Development)

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/blablablasealsaresoft/infofi.git
cd infofi
```

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Copy environment file
copy env.example .env

# Edit .env with your database credentials
# DATABASE_URL=postgresql://your_user:your_password@localhost:5432/infofi
```

### Step 3: Database Setup

```bash
# Create PostgreSQL database
psql -U postgres
CREATE DATABASE infofi;
\q

# Initialize database (tables will be created automatically on first run)
```

### Step 4: Start Redis

```bash
# Windows (if installed as service)
redis-server

# Or using WSL
wsl redis-server
```

### Step 5: Start Ollama

```bash
# Start Ollama service
ollama serve

# In another terminal, pull the model
ollama pull deepseek-r1
```

### Step 6: Run Backend

```bash
# From backend directory
python -m uvicorn app.main:app --reload

# Backend will be available at:
# http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Step 7: Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local

# Start development server
npm run dev

# Frontend will be available at:
# http://localhost:3000
```

## 🎯 First Steps After Setup

### 1. Create an Account

Visit http://localhost:3000 and:
- Click "Sign In"
- Click "Register"
- Create account with email or connect wallet

### 2. Start the Crawler

```bash
# In the project root directory
python harvest_research_data.py
```

This will populate the database with initial data from platforms.

### 3. Explore the Dashboard

- View active campaigns
- Check leaderboards
- Link your wallets
- Set up alerts

## 🔧 Troubleshooting

### Database Connection Error

```bash
# Check if PostgreSQL is running
psql --version
pg_ctl status

# Verify credentials in backend/.env
DATABASE_URL=postgresql://user:password@localhost:5432/infofi
```

### Redis Connection Error

```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG

# Start Redis if not running
redis-server
```

### Ollama Model Not Found

```bash
# List installed models
ollama list

# Pull the model if missing
ollama pull deepseek-r1
```

### Frontend Can't Connect to API

1. Check that backend is running on port 8000
2. Verify `NEXT_PUBLIC_API_URL` in `frontend/.env.local`
3. Check browser console for CORS errors
4. Restart both backend and frontend

### Port Already in Use

```bash
# Find process using port 8000 (backend)
netstat -ano | findstr :8000

# Kill the process (replace PID)
taskkill /PID <PID> /F

# Or change port in backend/app/main.py
uvicorn app.main:app --reload --port 8001
```

## 📚 Project Structure

```
infofi/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # REST API endpoints
│   │   ├── models/      # Database models
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Business logic
│   └── requirements.txt
│
├── frontend/            # Next.js frontend
│   ├── src/
│   │   ├── app/        # Next.js 14 App Router
│   │   ├── components/ # React components
│   │   └── lib/        # Utilities & API client
│   └── package.json
│
├── harvest_research_data.py  # Original crawler
├── docker-compose.yml         # Docker services
└── README.md
```

## 🧪 Running Tests

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 🔐 Security Notes

- Change `SECRET_KEY` in `backend/.env` before deploying
- Never commit `.env` files to Git
- Use environment variables for sensitive data
- Enable HTTPS in production
- Set strong database passwords

## 📖 Next Steps

1. **Read the Architecture** - [ARCHITECTURE.md](./ARCHITECTURE.md)
2. **Check the Roadmap** - [IMPLEMENTATION_CHECKLIST.md](./IMPLEMENTATION_CHECKLIST.md)
3. **Explore API Docs** - http://localhost:8000/docs
4. **Join Community** - Discord, Twitter (links in README)

## 🆘 Need Help?

- **Issues**: Open an issue on GitHub
- **Discord**: Join our community server
- **Email**: hello@infofi.xyz
- **Docs**: Full documentation in ARCHITECTURE.md

## 🌟 Ready to Contribute?

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

**Built with ❤️ by the InfoFi Team**

