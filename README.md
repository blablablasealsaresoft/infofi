# Crypto Research Data Harvester

This project is an automated data harvesting tool designed to scrape user profiles, leaderboards, and quest information from various crypto platforms (e.g., Galxe, Layer3, etc.). It leverages `crawl4ai` for deep web crawling and `twikit` for enriching user data with Twitter/X engagement metrics.

## Features

-   **Deep Crawling**: Uses BFS (Breadth-First Search) strategy to explore deep into websites to find user profiles and leaderboards.
-   **LLM Extraction**: Utilizes Large Language Models (LLMs) to intelligently extract structured data (usernames, ranks, scores, wallet addresses) from unstructured HTML.
-   **Twitter Enrichment**: Automatically finds linked Twitter handles and fetches engagement stats (followers, recent tweets, engagement score) to identify high-value users.
-   **Anti-Detection**: Includes a persistent browser profile setup and cookie management to bypass bot protections (like Cloudflare) on sites like Twitter.
-   **Data Export**: Saves extracted and enriched data into JSON files for further analysis.

## Prerequisites

-   Python 3.10+
-   A Twitter/X account (for enrichment features)

## Installation

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <your-repo-url>
    cd <repo-name>
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Crawl4AI**:
    ```bash
    crawl4ai-setup
    ```

4.  **Configure Environment**:
    Create a `.env` file in the root directory (optional but recommended for credentials):
    ```env
    TWITTER_USERNAME=your_username
    TWITTER_PASSWORD=your_password
    TWITTER_EMAIL=your_email
    ```
    *Note: The primary login method uses cookies, so this is a backup.*

## Usage

### 1. Authenticate with Twitter
To avoid login issues and captchas, run the cookie extraction script once. This launches a browser for you to manually log in.

```bash
python get_twitter_cookies.py
```
-   A browser window will open.
-   Log in to Twitter/X.
-   Once on your home feed, return to the terminal and press **Enter**.
-   Cookies will be saved to `twitter_cookies.json`.

### 2. Run the Harvester
Start the main scraping and enrichment process:

```bash
python harvest_research_data.py
```

The script will:
1.  Crawl the target URLs defined in `harvest_research_data.py`.
2.  Extract user data using the configured LLM strategy.
3.  Cross-reference found handles with Twitter data (if enabled).
4.  Save results to `*_data.json` files.

## Project Structure

-   `harvest_research_data.py`: Main script configuration and execution logic.
-   `get_twitter_cookies.py`: Helper tool to generate valid Twitter session cookies.
-   `test_twikit.py`: Simple test to verify Twitter API access.
-   `chrome_profile/`: Directory storing the persistent browser session (ignored by git).
