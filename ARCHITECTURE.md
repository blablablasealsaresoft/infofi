# InfoFi Platform - Technical Architecture Document

**Version:** 1.0  
**Date:** December 11, 2025  
**Status:** Living Document

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Overview](#system-overview)
3. [Technology Stack](#technology-stack)
4. [Architecture Diagrams](#architecture-diagrams)
5. [Database Design](#database-design)
6. [Backend Architecture](#backend-architecture)
7. [Frontend Architecture](#frontend-architecture)
8. [Data Pipeline](#data-pipeline)
9. [API Design](#api-design)
10. [Security Architecture](#security-architecture)
11. [Infrastructure & Deployment](#infrastructure--deployment)
12. [Scalability Strategy](#scalability-strategy)
13. [Monitoring & Observability](#monitoring--observability)
14. [Development Roadmap](#development-roadmap)

---

## 1. Executive Summary

InfoFi is a comprehensive intelligence platform that aggregates, analyzes, and surfaces actionable insights from the fragmented InfoFi ecosystem. The platform combines:

- **Multi-platform data harvesting** from 10+ crypto reputation platforms
- **Social graph enrichment** via Twitter/X API integration
- **AI-powered predictive analytics** using LLMs and ML models
- **Real-time monitoring** with sub-minute update latency
- **RESTful & WebSocket APIs** for third-party integration

**Key Metrics:**
- Support for 10+ platforms (Galxe, Layer3, Cookie, Kaito, etc.)
- Process 100K+ user profiles daily
- Sub-5-minute alerting for new campaigns
- 99.9% uptime SLA for paid tiers

---

## 2. System Overview

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Web App     │  │  Mobile App  │  │  API Clients │          │
│  │  (Next.js)   │  │  (React      │  │  (REST/WSS)  │          │
│  │              │  │   Native)    │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  NGINX / Cloudflare (Rate Limiting, DDoS Protection)     │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  FastAPI     │  │  WebSocket   │  │  Auth        │          │
│  │  REST API    │  │  Server      │  │  Service     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     SERVICE LAYER                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ Crawler  │ │Analytics │ │Prediction│ │Alerting  │           │
│  │ Service  │ │ Engine   │ │ Service  │ │ Service  │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │PostgreSQL│ │  Redis   │ │TimescaleDB│ │ S3/Blob │           │
│  │ (Primary)│ │ (Cache)  │ │(Time-Series)│ (Storage)│           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ Ollama   │ │ Twitter  │ │  Target  │ │  Stripe  │           │
│  │ (LLM)    │ │   API    │ │Platforms │ │ (Payment)│           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Core Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| **Web Frontend** | User-facing dashboard | Next.js 14, React, TailwindCSS |
| **API Server** | RESTful endpoints | FastAPI (Python 3.11+) |
| **WebSocket Server** | Real-time updates | FastAPI WebSockets |
| **Crawler Service** | Data harvesting | Crawl4AI, Playwright |
| **Analytics Engine** | Data processing & insights | Pandas, NumPy, scikit-learn |
| **Prediction Service** | ML-powered predictions | TensorFlow/PyTorch |
| **Alert Service** | Notifications | Celery, Redis Queue |
| **Database** | Persistent storage | PostgreSQL 15+ |
| **Cache Layer** | Performance optimization | Redis 7+ |
| **Time-Series DB** | Historical metrics | TimescaleDB |
| **Object Storage** | Raw HTML, screenshots | AWS S3 / MinIO |

---

## 3. Technology Stack

### 3.1 Backend Stack

```python
# Core Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0

# Database & ORM
sqlalchemy==2.0.25
asyncpg==0.29.0
alembic==1.13.1
psycopg2-binary==2.9.9

# Caching & Queue
redis==5.0.1
celery==5.3.6
celery[redis]==5.3.6

# Data Processing
pandas==2.2.0
numpy==1.26.3
scikit-learn==1.4.0

# Crawling & AI (existing)
crawl4ai>=0.7.7
twikit
ollama

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Monitoring
prometheus-client==0.19.0
sentry-sdk==1.40.0

# Utilities
httpx==0.26.0
python-dotenv==1.0.0
pytz==2024.1
```

### 3.2 Frontend Stack

```json
{
  "dependencies": {
    "next": "14.1.0",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "typescript": "5.3.3",
    
    "tailwindcss": "3.4.1",
    "shadcn/ui": "latest",
    "lucide-react": "0.312.0",
    
    "@tanstack/react-query": "5.17.19",
    "axios": "1.6.5",
    "socket.io-client": "4.6.1",
    
    "recharts": "2.10.4",
    "date-fns": "3.2.0",
    "zod": "3.22.4",
    "react-hook-form": "7.49.3",
    
    "wagmi": "2.5.7",
    "viem": "2.7.6",
    "@rainbow-me/rainbowkit": "2.0.2"
  }
}
```

### 3.3 Infrastructure

| Service | Technology | Purpose |
|---------|-----------|---------|
| **Hosting** | Railway / DigitalOcean | Application servers |
| **CDN** | Cloudflare | Static assets, DDoS protection |
| **Database** | Supabase / Railway | Managed PostgreSQL |
| **Cache** | Upstash Redis | Managed Redis |
| **Object Storage** | AWS S3 / Cloudflare R2 | File storage |
| **DNS** | Cloudflare | Domain management |
| **Email** | SendGrid / Resend | Transactional emails |
| **SMS/Telegram** | Twilio / Telegram Bot API | Alerts |
| **Monitoring** | Grafana Cloud | Metrics & logs |
| **Error Tracking** | Sentry | Exception monitoring |

---

## 4. Architecture Diagrams

### 4.1 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      DATA INGESTION FLOW                         │
└─────────────────────────────────────────────────────────────────┘

1. DISCOVERY PHASE
   ┌──────────────┐
   │ Cron Scheduler│ (Every 5 minutes)
   └───────┬───────┘
           │
           ▼
   ┌──────────────┐
   │ Crawler Queue│ (Redis)
   └───────┬───────┘
           │
           ▼
   ┌──────────────────────────────────┐
   │  Distributed Crawler Workers     │
   │  (Crawl4AI + Playwright)         │
   │  • Platform A Worker (3 instances)│
   │  • Platform B Worker (3 instances)│
   │  • Platform C Worker (3 instances)│
   └───────┬──────────────────────────┘
           │
           ▼

2. EXTRACTION PHASE
   ┌──────────────────────────────────┐
   │  LLM Extraction Service          │
   │  • DeepSeek-R1 (Ollama)          │
   │  • Schema validation (Pydantic)  │
   └───────┬──────────────────────────┘
           │
           ▼
   ┌──────────────┐
   │ Raw Data Lake│ (S3)
   │ • HTML       │
   │ • Screenshots│
   │ • Raw JSON   │
   └───────┬───────┘
           │
           ▼

3. ENRICHMENT PHASE
   ┌──────────────────────────────────┐
   │  Social Enrichment Service       │
   │  • Twitter API (Twikit)          │
   │  • Rate limiting (100 req/min)   │
   │  • Caching (Redis, 1hr TTL)      │
   └───────┬──────────────────────────┘
           │
           ▼

4. PROCESSING PHASE
   ┌──────────────────────────────────┐
   │  Data Processing Pipeline        │
   │  • Deduplication                 │
   │  • Normalization                 │
   │  • Cross-platform matching       │
   │  • Score calculation             │
   └───────┬──────────────────────────┘
           │
           ▼

5. STORAGE PHASE
   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
   │ PostgreSQL   │  │ TimescaleDB  │  │    Redis     │
   │ (Structured) │  │ (Time-Series)│  │   (Cache)    │
   └───────┬───────┘  └───────┬───────┘  └───────┬──────┘
           │                  │                  │
           └──────────────────┼──────────────────┘
                              ▼

6. DELIVERY PHASE
   ┌──────────────────────────────────┐
   │  API Layer & WebSockets          │
   │  • REST endpoints                │
   │  • Real-time updates             │
   │  • GraphQL (optional)            │
   └───────┬──────────────────────────┘
           │
           ▼
   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
   │  Web App     │  │ Mobile App   │  │ API Clients  │
   └──────────────┘  └──────────────┘  └──────────────┘
```

### 4.2 User Authentication Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION FLOW                           │
└─────────────────────────────────────────────────────────────────┘

User Login → Two Options:

OPTION 1: Email/Password
┌──────────────┐
│ User submits │
│ credentials  │
└───────┬───────┘
        ▼
┌──────────────────┐
│ FastAPI Auth     │
│ • Verify password│ (bcrypt)
│ • Generate JWT   │
└───────┬──────────┘
        ▼
┌──────────────────┐
│ Return tokens    │
│ • Access token   │ (15 min)
│ • Refresh token  │ (7 days)
└──────────────────┘

OPTION 2: Wallet Connect (Web3)
┌──────────────────┐
│ User connects    │
│ wallet (MetaMask)│
└───────┬──────────┘
        ▼
┌──────────────────┐
│ Sign message     │
│ "Login to InfoFi"│
│ Timestamp: XXX   │
└───────┬──────────┘
        ▼
┌──────────────────┐
│ Verify signature │
│ • Recover address│
│ • Check nonce    │
└───────┬──────────┘
        ▼
┌──────────────────┐
│ Create/link user │
│ • Store address  │
│ • Generate JWT   │
└──────────────────┘
```

---

## 5. Database Design

### 5.1 PostgreSQL Schema

```sql
-- ============================================================
-- USERS & AUTHENTICATION
-- ============================================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255), -- NULL if wallet-only auth
    username VARCHAR(50) UNIQUE NOT NULL,
    subscription_tier VARCHAR(20) DEFAULT 'free', -- free, pro, whale
    subscription_expires_at TIMESTAMP,
    api_key VARCHAR(64) UNIQUE,
    api_quota_remaining INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE TABLE user_wallets (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    wallet_address VARCHAR(42) UNIQUE NOT NULL,
    chain VARCHAR(20) DEFAULT 'ethereum', -- ethereum, polygon, etc.
    is_primary BOOLEAN DEFAULT FALSE,
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, wallet_address)
);

CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    refresh_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_expires_at ON user_sessions(expires_at);

-- ============================================================
-- PLATFORMS & CAMPAIGNS
-- ============================================================

CREATE TABLE platforms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL, -- galxe, layer3, cookie, etc.
    domain VARCHAR(255) NOT NULL,
    icon_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    crawler_config JSONB DEFAULT '{}'::jsonb,
    last_crawled_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    platform_id INT REFERENCES platforms(id),
    external_id VARCHAR(255), -- Platform's internal campaign ID
    name VARCHAR(500) NOT NULL,
    description TEXT,
    url VARCHAR(1000),
    campaign_type VARCHAR(50), -- quest, tournament, airdrop, etc.
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    total_participants INT DEFAULT 0,
    total_rewards_usd NUMERIC(15, 2),
    min_points_required INT,
    status VARCHAR(20) DEFAULT 'active', -- active, ended, upcoming
    discovered_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb,
    UNIQUE(platform_id, external_id)
);

CREATE INDEX idx_campaigns_platform_id ON campaigns(platform_id);
CREATE INDEX idx_campaigns_status ON campaigns(status);
CREATE INDEX idx_campaigns_end_date ON campaigns(end_date);

-- ============================================================
-- USER PROFILES & ACTIVITY
-- ============================================================

CREATE TABLE platform_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_wallet_id INT REFERENCES user_wallets(id) ON DELETE CASCADE,
    platform_id INT REFERENCES platforms(id),
    external_user_id VARCHAR(255), -- Platform's user ID
    username VARCHAR(255),
    display_name VARCHAR(255),
    profile_url VARCHAR(1000),
    avatar_url VARCHAR(500),
    total_points NUMERIC(15, 2) DEFAULT 0,
    global_rank INT,
    level INT,
    twitter_handle VARCHAR(100),
    discord_handle VARCHAR(100),
    last_synced_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb,
    UNIQUE(platform_id, external_user_id)
);

CREATE INDEX idx_platform_profiles_user_wallet_id ON platform_profiles(user_wallet_id);
CREATE INDEX idx_platform_profiles_platform_id ON platform_profiles(platform_id);
CREATE INDEX idx_platform_profiles_global_rank ON platform_profiles(global_rank);

CREATE TABLE campaign_participation (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
    platform_profile_id UUID REFERENCES platform_profiles(id) ON DELETE CASCADE,
    points_earned NUMERIC(15, 2) DEFAULT 0,
    rank INT,
    completion_percentage NUMERIC(5, 2),
    quests_completed INT DEFAULT 0,
    quests_total INT,
    first_activity_at TIMESTAMP,
    last_activity_at TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb,
    UNIQUE(campaign_id, platform_profile_id)
);

CREATE INDEX idx_campaign_participation_campaign_id ON campaign_participation(campaign_id);
CREATE INDEX idx_campaign_participation_profile_id ON campaign_participation(platform_profile_id);
CREATE INDEX idx_campaign_participation_rank ON campaign_participation(rank);

-- ============================================================
-- SOCIAL DATA (TWITTER)
-- ============================================================

CREATE TABLE twitter_profiles (
    id SERIAL PRIMARY KEY,
    twitter_handle VARCHAR(100) UNIQUE NOT NULL,
    twitter_id VARCHAR(50) UNIQUE,
    display_name VARCHAR(255),
    bio TEXT,
    followers_count INT DEFAULT 0,
    following_count INT DEFAULT 0,
    tweets_count INT DEFAULT 0,
    is_verified BOOLEAN DEFAULT FALSE,
    profile_image_url VARCHAR(500),
    last_synced_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE twitter_engagement (
    id BIGSERIAL PRIMARY KEY,
    twitter_profile_id INT REFERENCES twitter_profiles(id) ON DELETE CASCADE,
    tweet_id VARCHAR(50) UNIQUE NOT NULL,
    tweet_text TEXT,
    posted_at TIMESTAMP,
    likes_count INT DEFAULT 0,
    retweets_count INT DEFAULT 0,
    replies_count INT DEFAULT 0,
    quotes_count INT DEFAULT 0,
    engagement_score INT GENERATED ALWAYS AS 
        (likes_count + (retweets_count * 2) + (replies_count * 3) + (quotes_count * 2)) STORED,
    is_platform_related BOOLEAN DEFAULT FALSE,
    related_platforms VARCHAR(100)[], -- {galxe, layer3}
    sentiment VARCHAR(20), -- positive, neutral, negative
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_twitter_engagement_profile_id ON twitter_engagement(twitter_profile_id);
CREATE INDEX idx_twitter_engagement_posted_at ON twitter_engagement(posted_at);
CREATE INDEX idx_twitter_engagement_is_platform_related ON twitter_engagement(is_platform_related);

CREATE TABLE profile_twitter_link (
    platform_profile_id UUID REFERENCES platform_profiles(id) ON DELETE CASCADE,
    twitter_profile_id INT REFERENCES twitter_profiles(id) ON DELETE CASCADE,
    confidence_score NUMERIC(3, 2), -- 0.00 to 1.00
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY(platform_profile_id, twitter_profile_id)
);

-- ============================================================
-- ANALYTICS & SCORES
-- ============================================================

CREATE TABLE shill_scores (
    id BIGSERIAL PRIMARY KEY,
    platform_profile_id UUID REFERENCES platform_profiles(id) ON DELETE CASCADE,
    twitter_profile_id INT REFERENCES twitter_profiles(id) ON DELETE CASCADE,
    platform_id INT REFERENCES platforms(id),
    score NUMERIC(5, 2) NOT NULL, -- 0.00 to 100.00
    tweets_analyzed INT DEFAULT 0,
    avg_engagement INT DEFAULT 0,
    platform_correlation NUMERIC(3, 2), -- -1.00 to 1.00
    effectiveness_rating VARCHAR(20), -- low, medium, high, elite
    calculated_at TIMESTAMP DEFAULT NOW(),
    period_start TIMESTAMP,
    period_end TIMESTAMP
);

CREATE INDEX idx_shill_scores_profile_id ON shill_scores(platform_profile_id);
CREATE INDEX idx_shill_scores_calculated_at ON shill_scores(calculated_at);

CREATE TABLE roi_predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
    model_version VARCHAR(20),
    predicted_airdrop_value_usd NUMERIC(15, 2),
    predicted_time_investment_hours NUMERIC(10, 2),
    roi_per_hour NUMERIC(10, 2),
    confidence_score NUMERIC(3, 2), -- 0.00 to 1.00
    whale_concentration NUMERIC(3, 2), -- 0.00 to 1.00 (higher = more whales)
    recommendation VARCHAR(20), -- strong_buy, buy, hold, skip
    factors JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_roi_predictions_campaign_id ON roi_predictions(campaign_id);
CREATE INDEX idx_roi_predictions_recommendation ON roi_predictions(recommendation);

-- ============================================================
-- ALERTS & NOTIFICATIONS
-- ============================================================

CREATE TABLE user_alerts (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL, -- new_campaign, rank_change, whale_alert, etc.
    priority VARCHAR(20) DEFAULT 'medium', -- low, medium, high, critical
    title VARCHAR(255) NOT NULL,
    message TEXT,
    related_entity_type VARCHAR(50), -- campaign, profile, platform
    related_entity_id VARCHAR(100),
    is_read BOOLEAN DEFAULT FALSE,
    delivered_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user_alerts_user_id ON user_alerts(user_id);
CREATE INDEX idx_user_alerts_is_read ON user_alerts(is_read);
CREATE INDEX idx_user_alerts_created_at ON user_alerts(created_at);

CREATE TABLE user_alert_preferences (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    email_enabled BOOLEAN DEFAULT TRUE,
    telegram_enabled BOOLEAN DEFAULT FALSE,
    telegram_chat_id VARCHAR(50),
    push_enabled BOOLEAN DEFAULT FALSE,
    alert_types JSONB DEFAULT '{}'::jsonb, -- Which alerts to enable
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- CRAWLER & JOB TRACKING
-- ============================================================

CREATE TABLE crawler_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    platform_id INT REFERENCES platforms(id),
    job_type VARCHAR(50) NOT NULL, -- discovery, profile_sync, campaign_sync
    status VARCHAR(20) DEFAULT 'pending', -- pending, running, completed, failed
    priority INT DEFAULT 5, -- 1-10, higher = more priority
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    stats JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_crawler_jobs_status ON crawler_jobs(status);
CREATE INDEX idx_crawler_jobs_platform_id ON crawler_jobs(platform_id);
CREATE INDEX idx_crawler_jobs_created_at ON crawler_jobs(created_at);

-- ============================================================
-- API USAGE TRACKING
-- ============================================================

CREATE TABLE api_requests (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    api_key VARCHAR(64),
    endpoint VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INT,
    response_time_ms INT,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_api_requests_user_id ON api_requests(user_id);
CREATE INDEX idx_api_requests_api_key ON api_requests(api_key);
CREATE INDEX idx_api_requests_created_at ON api_requests(created_at);

-- ============================================================
-- TIMESCALEDB HYPERTABLES (for time-series data)
-- ============================================================

-- After creating TimescaleDB extension:
-- SELECT create_hypertable('twitter_engagement', 'posted_at');
-- SELECT create_hypertable('shill_scores', 'calculated_at');
-- SELECT create_hypertable('api_requests', 'created_at');
-- SELECT create_hypertable('crawler_jobs', 'created_at');
```

### 5.2 Redis Data Structures

```python
# Cache Keys Structure

# User session cache
user:session:{user_id} → {user_data} (TTL: 15 minutes)

# Platform profiles cache
profile:{platform_id}:{external_user_id} → {profile_data} (TTL: 1 hour)

# Campaign cache
campaign:{campaign_id} → {campaign_data} (TTL: 5 minutes)

# Leaderboard cache (sorted sets)
leaderboard:{platform_id}:{campaign_id} → ZSET(profile_id, score)

# Twitter rate limiting
twitter:ratelimit:{endpoint} → {remaining_calls} (TTL: 15 minutes)

# Crawler queue
queue:crawler:priority → LIST[job_id]
queue:crawler:normal → LIST[job_id]
queue:crawler:low → LIST[job_id]

# Real-time updates (pub/sub)
channel:alerts:{user_id} → pubsub
channel:leaderboard:{campaign_id} → pubsub

# API rate limiting (sliding window)
ratelimit:{api_key}:{window} → {request_count} (TTL: window duration)
```

---

## 6. Backend Architecture

### 6.1 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Settings & environment variables
│   ├── dependencies.py         # Shared dependencies (DB, auth, etc.)
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py         # Authentication endpoints
│   │   │   ├── users.py        # User management
│   │   │   ├── platforms.py    # Platform data
│   │   │   ├── campaigns.py    # Campaign endpoints
│   │   │   ├── profiles.py     # User profiles
│   │   │   ├── analytics.py    # Analytics & insights
│   │   │   ├── alerts.py       # Alert management
│   │   │   └── websocket.py    # WebSocket connections
│   │   └── deps.py             # API dependencies
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py         # JWT, hashing, encryption
│   │   ├── cache.py            # Redis caching layer
│   │   ├── rate_limit.py       # Rate limiting
│   │   └── monitoring.py       # Prometheus metrics
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # User SQLAlchemy models
│   │   ├── platform.py         # Platform models
│   │   ├── campaign.py         # Campaign models
│   │   ├── profile.py          # Profile models
│   │   ├── twitter.py          # Twitter models
│   │   └── alert.py            # Alert models
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # Pydantic schemas for users
│   │   ├── platform.py         # Platform schemas
│   │   ├── campaign.py         # Campaign schemas
│   │   ├── profile.py          # Profile schemas
│   │   ├── analytics.py        # Analytics schemas
│   │   └── common.py           # Shared schemas
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── crawler/
│   │   │   ├── __init__.py
│   │   │   ├── base.py         # Base crawler class
│   │   │   ├── manager.py      # Crawler orchestration
│   │   │   ├── platforms/
│   │   │   │   ├── galxe.py
│   │   │   │   ├── layer3.py
│   │   │   │   ├── cookie.py
│   │   │   │   └── ...
│   │   │   └── extractors.py   # LLM extraction logic
│   │   │
│   │   ├── social/
│   │   │   ├── __init__.py
│   │   │   ├── twitter.py      # Twitter enrichment
│   │   │   └── graph.py        # Social graph analysis
│   │   │
│   │   ├── analytics/
│   │   │   ├── __init__.py
│   │   │   ├── shill_score.py  # Shill score calculation
│   │   │   ├── roi_predictor.py # ML-based ROI prediction
│   │   │   └── insights.py     # General analytics
│   │   │
│   │   ├── alerts/
│   │   │   ├── __init__.py
│   │   │   ├── manager.py      # Alert orchestration
│   │   │   ├── email.py        # Email notifications
│   │   │   ├── telegram.py     # Telegram notifications
│   │   │   └── push.py         # Push notifications
│   │   │
│   │   └── payment/
│   │       ├── __init__.py
│   │       ├── stripe.py       # Stripe integration
│   │       └── subscription.py # Subscription management
│   │
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── celery_app.py       # Celery configuration
│   │   ├── crawler.py          # Crawler tasks
│   │   ├── enrichment.py       # Data enrichment tasks
│   │   └── analytics.py        # Analytics tasks
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py          # Database session
│   │   ├── base.py             # Base model
│   │   └── migrations/         # Alembic migrations
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py           # Logging configuration
│       ├── validators.py       # Custom validators
│       └── helpers.py          # Utility functions
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api/
│   ├── test_services/
│   └── test_utils/
│
├── scripts/
│   ├── seed_database.py
│   ├── migrate_data.py
│   └── benchmark.py
│
├── alembic.ini
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

### 6.2 Core Service Implementations

#### 6.2.1 Crawler Service Architecture

```python
# app/services/crawler/manager.py

from typing import List, Dict, Any
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.crawler.base import BaseCrawler
from app.services.crawler.platforms import (
    GalxeCrawler, Layer3Crawler, CookieCrawler
)
from app.models.crawler import CrawlerJob
from app.core.cache import cache_manager

class CrawlerManager:
    """Orchestrates multiple platform crawlers"""
    
    def __init__(self):
        self.crawlers: Dict[str, BaseCrawler] = {
            'galxe': GalxeCrawler(),
            'layer3': Layer3Crawler(),
            'cookie': CookieCrawler(),
        }
        self.running_jobs: Dict[str, asyncio.Task] = {}
    
    async def schedule_crawl(
        self, 
        platform: str,
        job_type: str,
        priority: int = 5
    ) -> str:
        """Schedule a new crawl job"""
        job = CrawlerJob(
            platform_id=platform,
            job_type=job_type,
            priority=priority
        )
        
        # Add to priority queue in Redis
        await cache_manager.add_to_queue(
            f"queue:crawler:priority:{priority}",
            str(job.id)
        )
        
        return str(job.id)
    
    async def execute_job(
        self,
        job_id: str,
        db: AsyncSession
    ):
        """Execute a crawler job"""
        job = await db.get(CrawlerJob, job_id)
        crawler = self.crawlers.get(job.platform_id)
        
        if not crawler:
            raise ValueError(f"No crawler for platform: {job.platform_id}")
        
        job.status = 'running'
        job.started_at = datetime.utcnow()
        await db.commit()
        
        try:
            if job.job_type == 'discovery':
                results = await crawler.discover_campaigns()
            elif job.job_type == 'profile_sync':
                results = await crawler.sync_profiles()
            elif job.job_type == 'campaign_sync':
                results = await crawler.sync_campaign_data(job.metadata.get('campaign_id'))
            
            job.status = 'completed'
            job.stats = results
        except Exception as e:
            job.status = 'failed'
            job.error_message = str(e)
            raise
        finally:
            job.completed_at = datetime.utcnow()
            await db.commit()
    
    async def run_scheduler(self):
        """Main scheduler loop"""
        while True:
            # Check for due crawls
            for platform_name, crawler in self.crawlers.items():
                last_crawl = await crawler.get_last_crawl_time()
                
                if not last_crawl or datetime.utcnow() - last_crawl > timedelta(minutes=5):
                    await self.schedule_crawl(platform_name, 'discovery', priority=8)
            
            await asyncio.sleep(60)  # Check every minute
```

#### 6.2.2 Analytics Service

```python
# app/services/analytics/shill_score.py

from typing import List, Dict
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.profile import PlatformProfile
from app.models.twitter import TwitterProfile, TwitterEngagement
from app.models.analytics import ShillScore

class ShillScoreCalculator:
    """Calculate shill effectiveness scores"""
    
    async def calculate_for_profile(
        self,
        platform_profile_id: str,
        db: AsyncSession,
        lookback_days: int = 30
    ) -> float:
        """
        Calculate shill score for a profile
        
        Score factors:
        - Tweet frequency about the platform
        - Engagement per tweet (likes + RTs + replies)
        - Correlation between tweet timing and point increases
        - Follower count (weighted less)
        """
        
        # Get platform profile and linked twitter
        profile = await db.get(PlatformProfile, platform_profile_id)
        
        stmt = select(TwitterProfile).join(
            profile_twitter_link
        ).where(
            profile_twitter_link.c.platform_profile_id == platform_profile_id
        )
        twitter = (await db.execute(stmt)).scalar_one_or_none()
        
        if not twitter:
            return 0.0
        
        # Get recent tweets
        cutoff = datetime.utcnow() - timedelta(days=lookback_days)
        stmt = select(TwitterEngagement).where(
            TwitterEngagement.twitter_profile_id == twitter.id,
            TwitterEngagement.posted_at >= cutoff,
            TwitterEngagement.is_platform_related == True
        )
        tweets = (await db.execute(stmt)).scalars().all()
        
        if not tweets:
            return 0.0
        
        # Calculate engagement metrics
        total_engagement = sum(t.engagement_score for t in tweets)
        avg_engagement = total_engagement / len(tweets)
        
        # Normalize by follower count (diminishing returns)
        follower_factor = np.log10(max(twitter.followers_count, 1)) / 5  # Cap at 2.0
        
        # Tweet frequency factor (1-10 tweets = optimal, more = spam)
        freq_factor = min(len(tweets) / 10, 1.0)
        if len(tweets) > 20:
            freq_factor *= 0.7  # Penalty for spam
        
        # Calculate correlation with point growth
        # (This would require time-series analysis of points)
        correlation_factor = await self._calculate_points_correlation(
            profile, tweets, db
        )
        
        # Final score (0-100)
        raw_score = (
            (avg_engagement / 100) * 40 +  # 40% weight on engagement
            freq_factor * 30 +              # 30% weight on frequency
            correlation_factor * 20 +       # 20% weight on correlation
            min(follower_factor, 1.0) * 10  # 10% weight on followers
        )
        
        score = min(raw_score, 100.0)
        
        # Save to database
        shill_score = ShillScore(
            platform_profile_id=platform_profile_id,
            twitter_profile_id=twitter.id,
            platform_id=profile.platform_id,
            score=score,
            tweets_analyzed=len(tweets),
            avg_engagement=int(avg_engagement),
            platform_correlation=correlation_factor,
            effectiveness_rating=self._get_rating(score),
            period_start=cutoff,
            period_end=datetime.utcnow()
        )
        
        db.add(shill_score)
        await db.commit()
        
        return score
    
    async def _calculate_points_correlation(
        self,
        profile: PlatformProfile,
        tweets: List[TwitterEngagement],
        db: AsyncSession
    ) -> float:
        """
        Calculate correlation between tweet activity and point increases
        This is a simplified version - would need time-series data
        """
        # Would implement time-series analysis here
        # For now, return a placeholder
        return 0.5
    
    def _get_rating(self, score: float) -> str:
        if score >= 80:
            return 'elite'
        elif score >= 60:
            return 'high'
        elif score >= 40:
            return 'medium'
        else:
            return 'low'
```

### 6.3 API Endpoint Examples

```python
# app/api/v1/analytics.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.services.analytics.shill_score import ShillScoreCalculator
from app.services.analytics.roi_predictor import ROIPredictor
from app.schemas.analytics import (
    ShillScoreResponse,
    ROIPrediction,
    LeaderboardEntry,
    PlatformComparison
)

router = APIRouter()

@router.get("/shill-score/{profile_id}", response_model=ShillScoreResponse)
async def get_shill_score(
    profile_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get shill score for a platform profile"""
    calculator = ShillScoreCalculator()
    score = await calculator.calculate_for_profile(profile_id, db)
    
    # Get detailed breakdown
    breakdown = await calculator.get_score_breakdown(profile_id, db)
    
    return ShillScoreResponse(
        profile_id=profile_id,
        score=score,
        rating=calculator._get_rating(score),
        breakdown=breakdown
    )

@router.get("/roi/campaign/{campaign_id}", response_model=ROIPrediction)
async def predict_campaign_roi(
    campaign_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Predict ROI for a campaign"""
    predictor = ROIPredictor()
    prediction = await predictor.predict(campaign_id, db)
    
    return prediction

@router.get("/leaderboard/global", response_model=List[LeaderboardEntry])
async def get_global_leaderboard(
    platform_id: Optional[int] = Query(None),
    limit: int = Query(100, le=1000),
    offset: int = Query(0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get global leaderboard across platforms"""
    # Implementation would aggregate from multiple platforms
    pass

@router.get("/comparison/{wallet_address}", response_model=PlatformComparison)
async def compare_platforms(
    wallet_address: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Compare user's performance across platforms"""
    # Implementation would fetch all profiles for this wallet
    pass
```

---

## 7. Frontend Architecture

### 7.1 Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   ├── register/
│   │   │   │   └── page.tsx
│   │   │   └── layout.tsx
│   │   │
│   │   ├── (dashboard)/
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx          # Main dashboard
│   │   │   ├── platforms/
│   │   │   │   ├── page.tsx          # Platform overview
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx      # Platform detail
│   │   │   ├── campaigns/
│   │   │   │   ├── page.tsx          # Campaign list
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx      # Campaign detail
│   │   │   ├── profiles/
│   │   │   │   ├── page.tsx          # User profiles
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx      # Profile detail
│   │   │   ├── analytics/
│   │   │   │   ├── page.tsx          # Analytics dashboard
│   │   │   │   ├── shill-score/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── roi/
│   │   │   │       └── page.tsx
│   │   │   ├── alerts/
│   │   │   │   └── page.tsx
│   │   │   ├── settings/
│   │   │   │   └── page.tsx
│   │   │   └── layout.tsx
│   │   │
│   │   ├── api/                      # API routes (if needed)
│   │   ├── layout.tsx                # Root layout
│   │   └── page.tsx                  # Landing page
│   │
│   ├── components/
│   │   ├── ui/                       # shadcn/ui components
│   │   ├── dashboard/
│   │   │   ├── stats-card.tsx
│   │   │   ├── platform-selector.tsx
│   │   │   ├── campaign-card.tsx
│   │   │   └── leaderboard-table.tsx
│   │   ├── analytics/
│   │   │   ├── shill-score-chart.tsx
│   │   │   ├── roi-calculator.tsx
│   │   │   └── trend-graph.tsx
│   │   ├── alerts/
│   │   │   ├── alert-list.tsx
│   │   │   └── alert-preferences.tsx
│   │   └── layout/
│   │       ├── header.tsx
│   │       ├── sidebar.tsx
│   │       └── footer.tsx
│   │
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.ts             # Axios client
│   │   │   ├── auth.ts               # Auth API
│   │   │   ├── platforms.ts          # Platform API
│   │   │   ├── campaigns.ts          # Campaign API
│   │   │   ├── profiles.ts           # Profile API
│   │   │   └── analytics.ts          # Analytics API
│   │   ├── hooks/
│   │   │   ├── use-auth.ts
│   │   │   ├── use-websocket.ts
│   │   │   ├── use-wallet.ts
│   │   │   └── use-alerts.ts
│   │   ├── utils/
│   │   │   ├── format.ts
│   │   │   ├── date.ts
│   │   │   └── validation.ts
│   │   ├── constants.ts
│   │   └── types.ts
│   │
│   ├── store/                        # State management (Zustand)
│   │   ├── auth-store.ts
│   │   ├── platform-store.ts
│   │   └── alert-store.ts
│   │
│   ├── styles/
│   │   └── globals.css
│   │
│   └── config/
│       ├── site.ts
│       └── wagmi.ts                  # Web3 config
│
├── public/
│   ├── images/
│   └── icons/
│
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.js
└── README.md
```

### 7.2 Key Frontend Components

#### 7.2.1 Dashboard Overview

```typescript
// src/app/(dashboard)/dashboard/page.tsx

'use client';

import { useQuery } from '@tanstack/react-query';
import { platformsApi, campaignsApi, analyticsApi } from '@/lib/api';
import { StatsCard } from '@/components/dashboard/stats-card';
import { LeaderboardTable } from '@/components/dashboard/leaderboard-table';
import { CampaignCard } from '@/components/dashboard/campaign-card';
import { ShillScoreChart } from '@/components/analytics/shill-score-chart';

export default function DashboardPage() {
  const { data: stats } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: () => analyticsApi.getDashboardStats(),
  });

  const { data: activeCampaigns } = useQuery({
    queryKey: ['campaigns', { status: 'active' }],
    queryFn: () => campaignsApi.list({ status: 'active', limit: 10 }),
  });

  const { data: topProfiles } = useQuery({
    queryKey: ['leaderboard', 'global'],
    queryFn: () => analyticsApi.getGlobalLeaderboard({ limit: 10 }),
  });

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground">
          Your InfoFi intelligence overview
        </p>
      </div>

      {/* Stats Overview */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatsCard
          title="Total Campaigns"
          value={stats?.totalCampaigns || 0}
          change="+12 this week"
          icon="trophy"
        />
        <StatsCard
          title="Your Rank (Avg)"
          value={`#${stats?.avgRank || '-'}`}
          change="↑ 15 positions"
          icon="trending-up"
        />
        <StatsCard
          title="Shill Score"
          value={stats?.shillScore || 0}
          change="Elite tier"
          icon="zap"
        />
        <StatsCard
          title="Est. Airdrop Value"
          value={`$${stats?.estimatedValue || 0}`}
          change="+$2.3k this month"
          icon="dollar-sign"
        />
      </div>

      {/* Active Campaigns */}
      <div>
        <h2 className="text-2xl font-bold mb-4">Hot Campaigns</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {activeCampaigns?.map((campaign) => (
            <CampaignCard key={campaign.id} campaign={campaign} />
          ))}
        </div>
      </div>

      {/* Leaderboard & Analytics */}
      <div className="grid gap-4 lg:grid-cols-2">
        <div>
          <h2 className="text-2xl font-bold mb-4">Global Leaders</h2>
          <LeaderboardTable profiles={topProfiles || []} />
        </div>
        <div>
          <h2 className="text-2xl font-bold mb-4">Your Shill Performance</h2>
          <ShillScoreChart />
        </div>
      </div>
    </div>
  );
}
```

#### 7.2.2 Real-time Updates with WebSocket

```typescript
// src/lib/hooks/use-websocket.ts

import { useEffect, useRef, useState } from 'react';
import { io, Socket } from 'socket.io-client';
import { useAuth } from './use-auth';

export function useWebSocket() {
  const { token } = useAuth();
  const [isConnected, setIsConnected] = useState(false);
  const socketRef = useRef<Socket>();

  useEffect(() => {
    if (!token) return;

    const socket = io(process.env.NEXT_PUBLIC_WS_URL!, {
      auth: { token },
    });

    socket.on('connect', () => {
      setIsConnected(true);
      console.log('WebSocket connected');
    });

    socket.on('disconnect', () => {
      setIsConnected(false);
      console.log('WebSocket disconnected');
    });

    socketRef.current = socket;

    return () => {
      socket.disconnect();
    };
  }, [token]);

  const subscribe = (event: string, callback: (data: any) => void) => {
    socketRef.current?.on(event, callback);
  };

  const unsubscribe = (event: string, callback?: (data: any) => void) => {
    if (callback) {
      socketRef.current?.off(event, callback);
    } else {
      socketRef.current?.off(event);
    }
  };

  return {
    isConnected,
    subscribe,
    unsubscribe,
  };
}

// Usage in a component
export function AlertBell() {
  const { subscribe, unsubscribe } = useWebSocket();
  const [newAlertCount, setNewAlertCount] = useState(0);

  useEffect(() => {
    const handleNewAlert = (alert: any) => {
      setNewAlertCount((prev) => prev + 1);
      // Show toast notification
      toast.success(alert.title);
    };

    subscribe('alert:new', handleNewAlert);

    return () => {
      unsubscribe('alert:new', handleNewAlert);
    };
  }, [subscribe, unsubscribe]);

  return (
    <button className="relative">
      <Bell className="h-5 w-5" />
      {newAlertCount > 0 && (
        <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
          {newAlertCount}
        </span>
      )}
    </button>
  );
}
```

---

## 8. Data Pipeline

### 8.1 Crawler Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    CRAWLER PIPELINE FLOW                         │
└─────────────────────────────────────────────────────────────────┘

STAGE 1: Job Scheduling (Cron / Manual Trigger)
  ↓
  [Redis Queue] → Prioritized job queue
  ↓

STAGE 2: Worker Pool (3-10 workers per platform)
  ↓
  [Playwright Browser] → Stealth browsing + session persistence
  ↓
  [Page Load] → Wait for dynamic content, handle infinite scroll
  ↓
  [HTML Extraction] → Raw HTML saved to S3 for debugging
  ↓

STAGE 3: LLM Extraction (Ollama DeepSeek-R1)
  ↓
  [Fit Markdown] → Convert HTML to optimized markdown
  ↓
  [Schema Extraction] → Extract structured data (Pydantic)
  ↓
  [Validation] → Ensure data quality
  ↓

STAGE 4: Social Enrichment (Twitter API via Twikit)
  ↓
  [Handle Matching] → Find Twitter profiles for on-chain identities
  ↓
  [Profile Fetch] → Get follower count, bio, verification
  ↓
  [Tweet Analysis] → Fetch recent tweets, calculate engagement
  ↓
  [Rate Limiting] → 100 requests/min, retry with backoff
  ↓

STAGE 5: Data Processing
  ↓
  [Deduplication] → Merge duplicate profiles across crawls
  ↓
  [Normalization] → Standardize formats (addresses, usernames)
  ↓
  [Cross-Platform Matching] → Link same user across platforms
  ↓
  [Score Calculation] → Calculate shill scores, rankings
  ↓

STAGE 6: Storage & Caching
  ↓
  [PostgreSQL] → Store structured data
  ↓
  [TimescaleDB] → Store time-series metrics
  ↓
  [Redis] → Cache frequently accessed data
  ↓

STAGE 7: Alerting & Notifications
  ↓
  [Change Detection] → Detect rank changes, new campaigns
  ↓
  [Alert Generation] → Create user-specific alerts
  ↓
  [Notification Dispatch] → Email, Telegram, Push
```

### 8.2 Real-time Update Pipeline

```python
# app/tasks/realtime_sync.py

from celery import Celery
from datetime import datetime
from app.core.websocket import websocket_manager
from app.services.analytics.shill_score import ShillScoreCalculator

celery_app = Celery('infofi')

@celery_app.task(name='sync_campaign_leaderboard')
async def sync_campaign_leaderboard(campaign_id: str):
    """
    Sync a campaign's leaderboard and push updates to connected clients
    """
    # Crawl latest data
    crawler = get_crawler_for_campaign(campaign_id)
    new_data = await crawler.get_leaderboard(campaign_id)
    
    # Detect changes
    old_data = await get_cached_leaderboard(campaign_id)
    changes = detect_rank_changes(old_data, new_data)
    
    # Store in database
    await store_leaderboard_snapshot(campaign_id, new_data)
    
    # Update cache
    await cache_leaderboard(campaign_id, new_data)
    
    # Push updates via WebSocket
    await websocket_manager.broadcast_to_campaign(
        campaign_id,
        {
            'type': 'leaderboard_update',
            'data': new_data,
            'changes': changes,
            'timestamp': datetime.utcnow().isoformat()
        }
    )
    
    # Generate alerts for rank changes
    for change in changes:
        if abs(change['rank_delta']) >= 10:  # Significant change
            await generate_rank_change_alert(
                user_id=change['user_id'],
                campaign_id=campaign_id,
                old_rank=change['old_rank'],
                new_rank=change['new_rank']
            )

@celery_app.task(name='recalculate_shill_scores')
async def recalculate_shill_scores():
    """
    Periodically recalculate shill scores for all active users
    """
    calculator = ShillScoreCalculator()
    
    # Get all profiles with linked Twitter accounts
    profiles = await get_profiles_with_twitter()
    
    for profile in profiles:
        try:
            new_score = await calculator.calculate_for_profile(
                profile.id,
                db,
                lookback_days=30
            )
            
            # Check if score changed significantly
            old_score = profile.latest_shill_score
            if abs(new_score - old_score) >= 5:
                # Notify user
                await websocket_manager.send_to_user(
                    profile.user_id,
                    {
                        'type': 'shill_score_update',
                        'profile_id': profile.id,
                        'old_score': old_score,
                        'new_score': new_score,
                        'change': new_score - old_score
                    }
                )
        except Exception as e:
            logger.error(f"Failed to calculate shill score for {profile.id}: {e}")
```

---

## 9. API Design

### 9.1 RESTful API Specification

**Base URL:** `https://api.infofi.xyz/v1`

#### Authentication Endpoints

```
POST   /auth/register
POST   /auth/login
POST   /auth/logout
POST   /auth/refresh
POST   /auth/wallet-login
GET    /auth/me
```

#### Platform Endpoints

```
GET    /platforms
GET    /platforms/{id}
GET    /platforms/{id}/campaigns
GET    /platforms/{id}/leaderboard
```

#### Campaign Endpoints

```
GET    /campaigns
GET    /campaigns/{id}
GET    /campaigns/{id}/participants
GET    /campaigns/{id}/my-position
GET    /campaigns/search
```

#### Profile Endpoints

```
GET    /profiles/me
GET    /profiles/{id}
GET    /profiles/{id}/campaigns
GET    /profiles/{id}/history
POST   /profiles/link-wallet
POST   /profiles/link-twitter
```

#### Analytics Endpoints

```
GET    /analytics/shill-score/{profile_id}
GET    /analytics/roi/campaign/{campaign_id}
GET    /analytics/leaderboard/global
GET    /analytics/comparison/{wallet_address}
GET    /analytics/trends
```

#### Alert Endpoints

```
GET    /alerts
POST   /alerts/preferences
GET    /alerts/unread-count
PUT    /alerts/{id}/read
DELETE /alerts/{id}
```

### 9.2 WebSocket Events

**Connection:** `wss://api.infofi.xyz/ws?token=<jwt_token>`

#### Client → Server Events

```typescript
// Subscribe to campaign updates
socket.emit('subscribe:campaign', { campaign_id: 'xxx' });

// Subscribe to personal alerts
socket.emit('subscribe:alerts');

// Unsubscribe
socket.emit('unsubscribe:campaign', { campaign_id: 'xxx' });
```

#### Server → Client Events

```typescript
// New campaign discovered
socket.on('campaign:new', (data) => {
  // data: { platform, campaign_id, name, ... }
});

// Leaderboard update
socket.on('leaderboard:update', (data) => {
  // data: { campaign_id, top_10, my_position, ... }
});

// Rank change alert
socket.on('alert:rank_change', (data) => {
  // data: { campaign_id, old_rank, new_rank, change }
});

// Shill score update
socket.on('shill_score:update', (data) => {
  // data: { profile_id, old_score, new_score }
});
```

---

## 10. Security Architecture

### 10.1 Authentication & Authorization

```python
# app/core/security.py

from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from eth_account.messages import encode_defunct
from web3 import Web3

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-secret-key"  # From environment
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_wallet_signature(
    wallet_address: str,
    message: str,
    signature: str
) -> bool:
    """Verify an Ethereum wallet signature"""
    w3 = Web3()
    message_hash = encode_defunct(text=message)
    recovered_address = w3.eth.account.recover_message(
        message_hash,
        signature=signature
    )
    return recovered_address.lower() == wallet_address.lower()
```

### 10.2 Rate Limiting

```python
# app/core/rate_limit.py

from fastapi import Request, HTTPException
from redis import Redis
from datetime import datetime, timedelta

redis_client = Redis.from_url("redis://localhost:6379")

class RateLimiter:
    """Sliding window rate limiter"""
    
    def __init__(
        self,
        requests: int,
        window: int,  # seconds
        key_prefix: str = "ratelimit"
    ):
        self.requests = requests
        self.window = window
        self.key_prefix = key_prefix
    
    async def check(self, identifier: str) -> bool:
        """Check if request is allowed"""
        key = f"{self.key_prefix}:{identifier}"
        now = datetime.utcnow().timestamp()
        window_start = now - self.window
        
        # Remove old entries
        redis_client.zremrangebyscore(key, 0, window_start)
        
        # Count requests in window
        request_count = redis_client.zcard(key)
        
        if request_count >= self.requests:
            return False
        
        # Add current request
        redis_client.zadd(key, {str(now): now})
        redis_client.expire(key, self.window)
        
        return True
    
    async def get_remaining(self, identifier: str) -> int:
        """Get remaining requests in window"""
        key = f"{self.key_prefix}:{identifier}"
        now = datetime.utcnow().timestamp()
        window_start = now - self.window
        
        redis_client.zremrangebyscore(key, 0, window_start)
        request_count = redis_client.zcard(key)
        
        return max(0, self.requests - request_count)

# Usage in FastAPI
from fastapi import Depends

api_limiter = RateLimiter(requests=100, window=60)  # 100 req/min

async def check_rate_limit(request: Request):
    identifier = request.state.user_id or request.client.host
    
    if not await api_limiter.check(identifier):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )
```

### 10.3 Data Protection

- **Encryption at Rest:** Database encryption via PostgreSQL pgcrypto
- **Encryption in Transit:** TLS 1.3 for all API connections
- **Sensitive Data:** API keys, passwords hashed with bcrypt
- **PII Handling:** Email addresses encrypted, optional for wallet-only users
- **Cookie Security:** httpOnly, secure, sameSite=strict

---

## 11. Infrastructure & Deployment

### 11.1 Docker Architecture

```yaml
# docker-compose.yml

version: '3.8'

services:
  # API Server
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/infofi
      - REDIS_URL=redis://redis:6379/0
      - OLLAMA_HOST=http://ollama:11434
    depends_on:
      - db
      - redis
      - ollama
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # Celery Worker (Crawler Jobs)
  worker:
    build: ./backend
    command: celery -A app.tasks.celery_app worker -Q crawler -c 5 --loglevel=info
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/infofi
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./backend:/app
      - ./chrome_profile:/app/chrome_profile

  # Celery Worker (Analytics)
  analytics_worker:
    build: ./backend
    command: celery -A app.tasks.celery_app worker -Q analytics -c 10 --loglevel=info
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/infofi
      - REDIS_URL=redis://redis:6379/0
      - OLLAMA_HOST=http://ollama:11434
    depends_on:
      - db
      - redis
      - ollama

  # Celery Beat (Scheduler)
  beat:
    build: ./backend
    command: celery -A app.tasks.celery_app beat --loglevel=info
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis

  # PostgreSQL
  db:
    image: timescale/timescaledb:latest-pg15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=infofi
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  # Redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # Ollama (LLM)
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    command: serve

  # NGINX (Reverse Proxy)
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api

volumes:
  postgres_data:
  redis_data:
  ollama_data:
```

### 11.2 Deployment Strategy

**Production Stack:**
- **Frontend:** Vercel (Next.js optimized, edge functions)
- **API:** Railway or DigitalOcean App Platform (auto-scaling)
- **Database:** Supabase or Railway (managed PostgreSQL + TimescaleDB)
- **Cache:** Upstash Redis (serverless)
- **Storage:** Cloudflare R2 or AWS S3
- **CDN:** Cloudflare (global edge network)
- **Monitoring:** Grafana Cloud + Sentry

**CI/CD Pipeline:**
```yaml
# .github/workflows/deploy.yml

name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest

  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Railway
        uses: railwayapp/railway-deploy@v1
        with:
          railway-token: ${{ secrets.RAILWAY_TOKEN }}

  deploy-frontend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
```

---

## 12. Scalability Strategy

### 12.1 Horizontal Scaling

```
┌─────────────────────────────────────────────────────────────────┐
│                     SCALABILITY ARCHITECTURE                     │
└─────────────────────────────────────────────────────────────────┘

LOAD BALANCER (Cloudflare / NGINX)
  ↓
┌─────────────────────────────────────────┐
│     API Server Pool (Auto-scaling)      │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│  │ API 1│ │ API 2│ │ API 3│ │ API N│   │
│  └──────┘ └──────┘ └──────┘ └──────┘   │
└─────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────┐
│    Worker Pool (Platform-specific)      │
│  ┌────────────────┐  ┌────────────────┐ │
│  │ Galxe Workers  │  │ Layer3 Workers │ │
│  │ (3-5 instances)│  │ (3-5 instances)│ │
│  └────────────────┘  └────────────────┘ │
└─────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────┐
│         Database Scaling                │
│  ┌──────────────┐  ┌──────────────────┐ │
│  │ Read Replicas│  │ Connection Pool  │ │
│  │ (3 instances)│  │ (PgBouncer)      │ │
│  └──────────────┘  └──────────────────┘ │
└─────────────────────────────────────────┘
```

### 12.2 Performance Optimization

**Caching Strategy:**
- L1: In-memory cache (application level) - 1 minute TTL
- L2: Redis cache - 5-60 minute TTL
- L3: Database (with indexes)

**Database Optimization:**
```sql
-- Partitioning for large tables
CREATE TABLE twitter_engagement_y2025m01 
PARTITION OF twitter_engagement 
FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

-- Materialized views for expensive queries
CREATE MATERIALIZED VIEW global_leaderboard AS
SELECT 
    pp.id,
    pp.username,
    pp.total_points,
    RANK() OVER (ORDER BY pp.total_points DESC) as rank
FROM platform_profiles pp
WHERE pp.last_synced_at > NOW() - INTERVAL '24 hours';

-- Refresh periodically
REFRESH MATERIALIZED VIEW CONCURRENTLY global_leaderboard;
```

**Query Optimization:**
- Implement GraphQL DataLoader for N+1 query prevention
- Use database connection pooling (PgBouncer)
- Implement query result caching
- Use database read replicas for heavy read operations

---

## 13. Monitoring & Observability

### 13.1 Metrics to Track

```python
# app/core/monitoring.py

from prometheus_client import Counter, Histogram, Gauge

# API Metrics
api_requests_total = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

api_request_duration = Histogram(
    'api_request_duration_seconds',
    'API request duration',
    ['method', 'endpoint']
)

# Crawler Metrics
crawler_jobs_total = Counter(
    'crawler_jobs_total',
    'Total crawler jobs',
    ['platform', 'status']
)

crawler_job_duration = Histogram(
    'crawler_job_duration_seconds',
    'Crawler job duration',
    ['platform']
)

profiles_scraped = Counter(
    'profiles_scraped_total',
    'Total profiles scraped',
    ['platform']
)

# Database Metrics
db_connection_pool_size = Gauge(
    'db_connection_pool_size',
    'Database connection pool size'
)

db_query_duration = Histogram(
    'db_query_duration_seconds',
    'Database query duration',
    ['query_type']
)

# Business Metrics
active_users_total = Gauge(
    'active_users_total',
    'Total active users',
    ['subscription_tier']
)

campaigns_active = Gauge(
    'campaigns_active',
    'Active campaigns',
    ['platform']
)
```

### 13.2 Logging Strategy

```python
# app/utils/logger.py

import logging
from pythonjsonlogger import jsonlogger

def setup_logging():
    logger = logging.getLogger()
    
    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)
    
    return logger

# Usage
logger = setup_logging()

logger.info(
    "Crawler job completed",
    extra={
        "platform": "galxe",
        "job_id": job_id,
        "profiles_found": 150,
        "duration_seconds": 45.2
    }
)
```

### 13.3 Alerting Rules

```yaml
# alerting_rules.yml (for Prometheus Alertmanager)

groups:
  - name: infofi_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(api_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "API error rate is {{ $value }} req/s"

      - alert: CrawlerJobsFailing
        expr: rate(crawler_jobs_total{status="failed"}[10m]) > 0.1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Crawler jobs failing frequently"

      - alert: DatabaseConnectionPoolExhausted
        expr: db_connection_pool_size > 90
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Database connection pool near capacity"
```

---

## 14. Development Roadmap

### Phase 1: MVP (Weeks 1-4)

**Week 1: Foundation**
- [ ] Setup project structure (backend + frontend)
- [ ] Database schema implementation
- [ ] Basic authentication (email + password)
- [ ] Migrate existing crawler to new architecture

**Week 2: Core Features**
- [ ] Platform management endpoints
- [ ] Campaign discovery & syncing
- [ ] Basic dashboard UI
- [ ] Profile linking (wallet connect)

**Week 3: Analytics**
- [ ] Shill score calculation
- [ ] Leaderboard aggregation
- [ ] Basic charts & visualizations
- [ ] Alert system (basic)

**Week 4: Polish & Launch**
- [ ] Testing & bug fixes
- [ ] Documentation
- [ ] Deploy to production
- [ ] Launch beta (invite-only)

### Phase 2: Growth (Weeks 5-8)

**Week 5-6: Advanced Features**
- [ ] ROI prediction model
- [ ] Multi-wallet tracking
- [ ] Advanced filtering & search
- [ ] Telegram bot integration

**Week 7-8: Monetization**
- [ ] Stripe integration
- [ ] Subscription tiers
- [ ] API key management
- [ ] Usage analytics

### Phase 3: Scale (Weeks 9-12)

**Week 9-10: Performance**
- [ ] Horizontal scaling
- [ ] Caching optimization
- [ ] Database optimization
- [ ] Mobile app (React Native)

**Week 11-12: Enterprise**
- [ ] White-label solution
- [ ] Advanced API features
- [ ] Custom integrations
- [ ] SLA guarantees

---

## Appendices

### A. Environment Variables

```bash
# .env.example

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/infofi
DATABASE_POOL_SIZE=20

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here
API_KEY_SALT=your-salt-here

# LLM
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=deepseek-r1

# Twitter API
TWITTER_COOKIES_PATH=./twitter_cookies.json

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Monitoring
SENTRY_DSN=https://...
GRAFANA_API_KEY=...

# External Services
SENDGRID_API_KEY=...
TELEGRAM_BOT_TOKEN=...

# Feature Flags
ENABLE_WEBSOCKETS=true
ENABLE_ROI_PREDICTIONS=true
ENABLE_TELEGRAM_ALERTS=false
```

### B. API Response Examples

```json
// GET /campaigns/{id}
{
  "id": "uuid-here",
  "platform": {
    "id": 1,
    "name": "Galxe",
    "icon_url": "https://..."
  },
  "name": "Galxe Spring Campaign 2025",
  "description": "Complete quests to earn points...",
  "url": "https://galxe.com/campaigns/...",
  "campaign_type": "quest",
  "start_date": "2025-01-01T00:00:00Z",
  "end_date": "2025-03-31T23:59:59Z",
  "total_participants": 15420,
  "total_rewards_usd": 50000,
  "status": "active",
  "my_participation": {
    "rank": 342,
    "points_earned": 1250,
    "completion_percentage": 65.5
  },
  "roi_prediction": {
    "estimated_airdrop_value_usd": 125.50,
    "predicted_time_investment_hours": 8.5,
    "roi_per_hour": 14.76,
    "recommendation": "buy",
    "confidence_score": 0.82
  }
}
```

---

**Document Version:** 1.0  
**Last Updated:** December 11, 2025  
**Maintained By:** InfoFi Core Team

---

This architecture is designed to scale from MVP to millions of users while maintaining performance, security, and reliability. Each component can be developed and deployed independently, allowing for rapid iteration and continuous improvement.

