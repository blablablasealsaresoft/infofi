# ⚡ QuickStart Guide

Get InfoFi running in **under 5 minutes** using Docker.

## Prerequisites

- [Docker Desktop](https://www.docker.com/get-started/) installed
- [Ollama](https://ollama.com/) installed

## Steps

### 1. Clone the Repository

```bash
git clone https://github.com/blablablasealsaresoft/infofi.git
cd infofi
```

### 2. Pull AI Model

```bash
ollama pull deepseek-r1
```

### 3. Start Services

```bash
docker-compose up -d
```

### 4. Access the Platform

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Next Steps

1. Create an account at http://localhost:3000
2. Run the crawler: `python harvest_research_data.py`
3. Explore the dashboard

## Stop Services

```bash
docker-compose down
```

## View Logs

```bash
docker-compose logs -f api
```

---

📖 For detailed setup instructions, see [GETTING_STARTED.md](./GETTING_STARTED.md)

