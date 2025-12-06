"""
News Tweet Generator - Main Flask Application
=============================================
A mobile-friendly web app that scrapes news from multiple sources
and generates tweet-sized summaries (max 270 characters) with related images.

HOW TO RUN:
-----------
1. Set up the OPENAI_API_KEY environment variable in Replit Secrets
2. Click Run or execute: python app.py
3. Open the webview to see the app

ENVIRONMENT VARIABLES:
---------------------
- OPENAI_API_KEY: Required for generating tweet summaries
- SESSION_SECRET: For Flask session management (auto-generated if not set)
"""

import os
from flask import Flask, render_template, jsonify, request
from news_sources import NEWS_SOURCES, CATEGORIES, scrape_article
from tweet_generator import generate_tweet

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

@app.route('/')
def home():
    """Home screen - displays grid of news source buttons"""
    return render_template('index.html', sources=NEWS_SOURCES)

@app.route('/source/<source_id>')
def source_page(source_id):
    """Source-specific screen with category buttons"""
    source = next((s for s in NEWS_SOURCES if s['id'] == source_id), None)
    if not source:
        return render_template('error.html', message="News source not found"), 404
    return render_template('source.html', source=source, categories=CATEGORIES)

@app.route('/api/generate', methods=['POST'])
def generate_news_tweet():
    """
    API endpoint to scrape news and generate tweet.
    
    Request JSON:
    - source_id: ID of the news source
    - category: Category of news (top, politics, sports, tech, international, random)
    
    Response JSON:
    - success: boolean
    - tweet_text: Generated tweet (max 270 chars)
    - image_url: URL of the article image
    - headline: Original article headline
    - source_name: Name of the news source
    - error: Error message if failed
    """
    try:
        data = request.get_json()
        source_id = data.get('source_id')
        category = data.get('category', 'top')
        
        source = next((s for s in NEWS_SOURCES if s['id'] == source_id), None)
        if not source:
            return jsonify({
                'success': False,
                'error': 'Invalid news source'
            }), 400
        
        article = scrape_article(source, category)
        
        if not article or not article.get('headline'):
            return jsonify({
                'success': False,
                'error': f'Could not fetch article from {source["name"]}. Please try again.'
            }), 500
        
        tweet_text = generate_tweet(
            headline=article['headline'],
            description=article.get('description', ''),
            source_name=source['name']
        )
        
        return jsonify({
            'success': True,
            'tweet_text': tweet_text,
            'image_url': article.get('image_url', ''),
            'headline': article['headline'],
            'source_name': source['name']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }), 500

@app.route('/manifest.json')
def manifest():
    """PWA manifest for Add to Home Screen functionality"""
    return jsonify({
        "name": "News Tweet Generator",
        "short_name": "NewsTweet",
        "description": "Generate tweet-sized news summaries with images",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#c5e41981",
        "theme_color": "#1371e4",
        "icons": [
            {
                "src": "/static/static/icon1.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/static/static/icon1.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    })

@app.route('/sw.js')
def service_worker():
    """Service worker for PWA functionality"""
    return app.send_static_file('sw.js'), 200, {'Content-Type': 'application/javascript'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
