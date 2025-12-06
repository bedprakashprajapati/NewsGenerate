"""
News Sources - Using GNews API (works on PythonAnywhere free tier)
"""

import requests
import random

# Get a free API key from https://gnews.io/ (100 requests/day free)
GNEWS_API_KEY = "14e37363b728bf5ca584076a51794cf2"  # Replace with your key

NEWS_SOURCES = [
    {'id': 'bbc', 'name': 'BBC', 'color': '#BB1919', 'domain': 'bbc.com'},
    {'id': 'cnn', 'name': 'CNN', 'color': '#CC0000', 'domain': 'cnn.com'},
    {'id': 'aljazeera', 'name': 'Al Jazeera', 'color': '#D2691E', 'domain': 'aljazeera.com'},
    {'id': 'ndtv', 'name': 'NDTV', 'color': '#E31E24', 'domain': 'ndtv.com'},
    {'id': 'toi', 'name': 'Times of India', 'color': '#E31837', 'domain': 'timesofindia.indiatimes.com'},
    {'id': 'indiatoday', 'name': 'India Today', 'color': '#E31E24', 'domain': 'indiatoday.in'},
    {'id': 'general', 'name': 'All Sources', 'color': '#1E3A8A', 'domain': None},
]

CATEGORIES = [
    {'id': 'random', 'name': 'Generate News', 'icon': '🔄'},
    {'id': 'general', 'name': 'Top News', 'icon': '📰'},
    {'id': 'world', 'name': 'International', 'icon': '🌍'},
    {'id': 'nation', 'name': 'National', 'icon': '🏛️'},
    {'id': 'sports', 'name': 'Sports', 'icon': '⚽'},
    {'id': 'technology', 'name': 'Tech', 'icon': '💻'},
    {'id': 'entertainment', 'name': 'Entertainment', 'icon': '🎬'},
    {'id': 'business', 'name': 'Business', 'icon': '💼'},
]

INSHORTS_CATEGORIES = CATEGORIES  # Keep compatibility

def scrape_article(source, category='general'):
    """Fetch news using GNews API"""
    try:
        # Map category
        if category == 'random':
            category = random.choice(['general', 'world', 'sports', 'technology', 'business'])
        if category == 'top':
            category = 'general'
        if category == 'international':
            category = 'world'
        if category == 'tech':
            category = 'technology'
        if category == 'politics':
            category = 'nation'

        # Build API URL
        base_url = "https://gnews.io/api/v4/top-headlines"
        params = {
            'apikey': GNEWS_API_KEY,
            'topic': category,
            'lang': 'en',
            'max': 10
        }

        # Filter by source domain if specified
        domain = source.get('domain')
        if domain:
            params['in'] = domain

        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        articles = data.get('articles', [])
        if not articles:
            # Fallback: try without domain filter
            if 'in' in params:
                del params['in']
                response = requests.get(base_url, params=params, timeout=15)
                data = response.json()
                articles = data.get('articles', [])

        if articles:
            # Pick random article from results
            article = random.choice(articles[:10])
            return {
                'headline': article.get('title', ''),
                'description': article.get('description', ''),
                'image_url': article.get('image', ''),
                'article_url': article.get('url', '')
            }

        return None

    except Exception as e:
        print(f"Error fetching news: {e}")
        return None
