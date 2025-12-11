# InfoFi Intelligence Platform

**InfoFi** is an advanced intelligence platform designed to aggregate, analyze, and surface actionable insights from the fragmented world of "InfoFi" (Information Finance). By combining deep web crawling of crypto platforms with real-time Twitter/X engagement metrics, InfoFi provides users with a comprehensive view of the most valuable activities, users, and trends in the space.

## 🚀 Product Vision

The goal of InfoFi is to be the single source of truth for on-chain and off-chain reputation, activity, and value. Instead of manually checking dozens of leaderboards and Twitter threads, users can access a unified product that answers questions like:
*   "Which users are top performers across multiple platforms (Galxe, Layer3, etc.)?"
*   "Does high Twitter engagement correlate with leaderboard success?"
*   "Who are the real influential 'shillers' versus organic users?"

## ⚡ Key Features

*   **Multi-Platform Data Harvesting**: Automatically scrapes and structures data from major InfoFi platforms:
    *   **Galxe**: Quests, campaigns, and user points.
    *   **Layer3**: Leaderboards, quest completion rates, and XP.
    *   **Cookie.fun**: Tracking marketing/KOL effectiveness.
    *   **Kaito.ai**: Sentiment and "mindshare" metrics.
    *   **Wallchain**: Wallet profitability and activity.
    *   **Xeet.ai**: Emerging trend data.
*   **Deep Social Enrichment**: Cross-references on-chain profiles with their Twitter/X identities to fetch:
    *   Follower counts & verification status.
    *   Recent tweet engagement (likes, retweets).
    *   "Shill Factor" analysis (correlation between tweets and points).
*   **LLM-Powered Extraction**: Uses `DeepSeek-R1` (via Ollama) to intelligently parse unstructured HTML, ensuring high-quality data even when website layouts change.
*   **Anti-Detection Engine**: Features a persistent, human-mimicking browser profile to bypass sophisticated bot protections (Cloudflare, etc.).

## 🛠️ Technology Stack

*   **Core**: Python 3.10+
*   **Crawling**: `Crawl4AI` (AsyncWebCrawler, BFS Deep Crawl)
*   **Browser Automation**: `Playwright` (with stealth plugins)
*   **Social Data**: `Twikit` (Twitter private API client)
*   **AI/LLM**: `Ollama` (DeepSeek-R1 model) for schema extraction

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/blablablasealsaresoft/infofi.git
    cd infofi
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Browsers**:
    ```bash
    crawl4ai-setup
    ```

## 🚦 Usage

### 1. Authenticate Social Layers
To enable deep Twitter analysis without getting blocked, run the one-time authentication script:
```bash
python get_twitter_cookies.py
```
*   This opens a secure browser window.
*   Log in to Twitter/X manually.
*   Press **Enter** in the terminal to save your session cookies safely.

### 2. Launch the Harvester
Start the intelligence gathering engine:
```bash
python harvest_research_data.py
```
The system will:
*   Crawl all configured target URLs.
*   Extract user profiles and leaderboards.
*   Enrich every profile with social stats.
*   Generate a correlation report (Points vs. Engagement).
*   Save structured data to `*_data.json`.

## 📊 Data Output
The platform generates rich JSON datasets containing:
*   `username` / `wallet_address`
*   `platform_score` (XP/Points)
*   `leaderboard_rank`
*   `twitter_stats` (Followers, Tweets)
*   `engagement_score` (Aggregate social impact)

---
*Built for the future of on-chain reputation.*
