"""
News Sources - Using NewsData.io API (works on PythonAnywhere free tier)
========================================================================
Get your FREE API key from: https://newsdata.io/ (200 requests/day)

Features:
- Trending/Breaking news
- India-specific news
- Multiple categories
- Images included
"""

import requests
import random

# Get a free API key from https://newsdata.io/ (200 requests/day free)
NEWSDATA_API_KEY = "pub_92a91dfa207f4fbfbfb68d7461bbd3ba"  # Replace with your key

NEWS_SOURCES = [
    {'id': 'trending', 'name': '🔥 Trending', 'color': '#FF4500', 'country': None, 'priority': 'top'},
    {'id': 'india', 'name': '🇮🇳 India', 'color': '#FF9933', 'country': 'in', 'priority': None},
    {'id': 'world', 'name': '🌍 World', 'color': '#1E3A8A', 'country': None, 'priority': None},
    {'id': 'us', 'name': '🇺🇸 USA', 'color': '#3C3B6E', 'country': 'us', 'priority': None},
    {'id': 'uk', 'name': '🇬🇧 UK', 'color': '#012169', 'country': 'gb', 'priority': None},
    {'id': 'bbc', 'name': 'BBC', 'color': '#BB1919', 'domain': 'bbc', 'country': None},
    {'id': 'cnn', 'name': 'CNN', 'color': '#CC0000', 'domain': 'cnn', 'country': None},
    {'id': 'toi', 'name': 'Times of India', 'color': '#E31837', 'domain': 'timesofindia', 'country': 'in'},
    {'id': 'ndtv', 'name': 'NDTV', 'color': '#E31E24', 'domain': 'ndtv', 'country': 'in'},
    {'id': 'indiatoday', 'name': 'India Today', 'color': '#E31E24', 'domain': 'indiatoday', 'country': 'in'},
    {'id': 'hindustantimes', 'name': 'Hindustan Times', 'color': '#0066B3', 'domain': 'hindustantimes', 'country': 'in'},
    {'id': 'aljazeera', 'name': 'Al Jazeera', 'color': '#D2691E', 'domain': 'aljazeera', 'country': None},
]

CATEGORIES = [
    {'id': 'random', 'name': 'Generate News', 'icon': '🔄'},
    {'id': 'top', 'name': 'Top News', 'icon': '📰'},
    {'id': 'politics', 'name': 'Politics', 'icon': '🏛️'},
    {'id': 'sports', 'name': 'Sports', 'icon': '⚽'},
    {'id': 'technology', 'name': 'Tech', 'icon': '💻'},
    {'id': 'business', 'name': 'Business', 'icon': '💼'},
    {'id': 'entertainment', 'name': 'Entertainment', 'icon': '🎬'},
    {'id': 'world', 'name': 'World', 'icon': '🌍'},
    {'id': 'science', 'name': 'Science', 'icon': '🔬'},
    {'id': 'health', 'name': 'Health', 'icon': '🏥'},
]

# Keep compatibility with existing code
INSHORTS_CATEGORIES = CATEGORIES


def scrape_article(source, category='top'):
    """
    Fetch news using NewsData.io API
    
    Args:
        source: Source dict from NEWS_SOURCES
        category: Category ID from CATEGORIES
    
    Returns:
        Dict with headline, description, image_url, article_url
        or None if failed
    """
    try:
        # Handle random category
        if category == 'random':
            category = random.choice(['top', 'politics', 'sports', 'technology', 'business', 'entertainment', 'world'])
        
        # Map categories to NewsData.io format
        category_map = {
            'top': 'top',
            'politics': 'politics',
            'sports': 'sports',
            'technology': 'technology',
            'tech': 'technology',
            'business': 'business',
            'entertainment': 'entertainment',
            'world': 'world',
            'science': 'science',
            'health': 'health',
            'international': 'world',
        }
        
        api_category = category_map.get(category, 'top')
        
        # Build API URL
        base_url = "https://newsdata.io/api/1/latest"
        params = {
            'apikey': NEWSDATA_API_KEY,
            'language': 'en',
        }
        
        # Add category (NewsData uses 'category' parameter)
        if api_category != 'top':
            params['category'] = api_category
        
        # Add country filter if source has it
        country = source.get('country')
        if country:
            params['country'] = country
        
        # Add domain filter if source has specific domain
        domain = source.get('domain')
        if domain:
            params['domain'] = domain
        
        # Add priority for trending news
        priority = source.get('priority')
        if priority:
            params['prioritydomain'] = priority
        
        # Make API request
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        # Check for errors
        if data.get('status') != 'success':
            print(f"API Error: {data.get('message', 'Unknown error')}")
            # Try fallback without filters
            return fallback_fetch(api_category)
        
        articles = data.get('results', [])
        
        if not articles:
            # Fallback: try without domain/country filter
            return fallback_fetch(api_category)
        
        # Filter articles that have images
        articles_with_images = [a for a in articles if a.get('image_url')]
        
        if articles_with_images:
            article = random.choice(articles_with_images[:10])
        else:
            article = random.choice(articles[:10])
        
        return {
            'headline': article.get('title', ''),
            'description': article.get('description', '') or article.get('content', '')[:200] if article.get('content') else '',
            'image_url': article.get('image_url', ''),
            'article_url': article.get('link', ''),
            'source_name': article.get('source_id', ''),
            'pubDate': article.get('pubDate', '')
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None


def fallback_fetch(category='top'):
    """Fallback fetch without filters if main request fails"""
    try:
        base_url = "https://newsdata.io/api/1/latest"
        params = {
            'apikey': NEWSDATA_API_KEY,
            'language': 'en',
            'country': 'in,us,gb',  # Mix of countries
        }
        
        if category != 'top':
            params['category'] = category
        
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        articles = data.get('results', [])
        if articles:
            articles_with_images = [a for a in articles if a.get('image_url')]
            if articles_with_images:
                article = random.choice(articles_with_images[:10])
            else:
                article = random.choice(articles[:10])
            
            return {
                'headline': article.get('title', ''),
                'description': article.get('description', '') or '',
                'image_url': article.get('image_url', ''),
                'article_url': article.get('link', ''),
            }
        return None
    except Exception as e:
        print(f"Fallback error: {e}")
        return None


def get_trending_news():
    """Get trending/breaking news specifically"""
    try:
        base_url = "https://newsdata.io/api/1/latest"
        params = {
            'apikey': NEWSDATA_API_KEY,
            'language': 'en',
            'prioritydomain': 'top',  # Get from top priority domains
        }
        
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        articles = data.get('results', [])
        if articles:
            articles_with_images = [a for a in articles if a.get('image_url')]
            if articles_with_images:
                return random.choice(articles_with_images[:10])
            return random.choice(articles[:10])
        return None
    except Exception as e:
        print(f"Trending news error: {e}")
        return None
