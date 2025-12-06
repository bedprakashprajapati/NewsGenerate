# News Tweet Generator

A mobile-friendly Progressive Web App that scrapes live news from multiple sources and generates tweet-sized summaries (max 270 characters) with related images.

## Overview

This app allows you to:
1. Select from 10+ news sources (BBC, CNN, NDTV, Times of India, etc.)
2. Choose a news category (Top, Politics, Sports, Tech, International, or Random)
3. Get AI-generated tweet summaries with the article's image
4. Copy the tweet and image URL with one tap

## Project Structure

```
├── app.py              # Main Flask application
├── news_sources.py     # News source configurations and scraping functions
├── tweet_generator.py  # OpenAI-powered tweet generation
├── templates/          # HTML templates
│   ├── base.html      # Base template with styles
│   ├── index.html     # Home screen with source grid
│   ├── source.html    # Source detail with categories
│   └── error.html     # Error page
├── static/            # Static files
│   ├── sw.js          # Service worker for PWA
│   └── icon-*.png     # PWA icons
└── replit.md          # This file
```

## Configuration

### Adding New News Sources

Edit `news_sources.py` and add to the `NEWS_SOURCES` list:

```python
{
    'id': 'source_id',        # unique lowercase ID
    'name': 'Source Name',     # display name
    'base_url': 'https://...',
    'color': '#HEXCOLOR',
    'urls': {
        'top': 'https://...',
        'politics': 'https://...',
        # ... more categories
    }
}
```

### Modifying Categories

Edit the `CATEGORIES` list in `news_sources.py`.

### Adjusting Tweet Length

Change `MAX_TWEET_LENGTH` in `tweet_generator.py` (default: 270 characters).

## Environment Variables

- `OPENAI_API_KEY` - Required for tweet generation (set in Replit Secrets)
- `SESSION_SECRET` - Flask session key (auto-generated if not set)

## Running the App

1. Click Run or execute `python app.py`
2. Open the webview URL
3. On mobile: Add to Home Screen for app-like experience

## Technical Details

- **Backend**: Flask (Python)
- **Scraping**: BeautifulSoup4 + requests
- **AI**: OpenAI GPT-4o-mini for tweet generation
- **Frontend**: Responsive HTML/CSS/JS
- **PWA**: Service worker + manifest for offline support

## Recent Changes

- Initial setup with 10 news sources
- Mobile-optimized UI with dark theme
- Copy to clipboard functionality
- PWA support for "Add to Home Screen"
