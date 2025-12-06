"""
News Sources Configuration and Scraping Module
===============================================
This module contains all news source configurations and scraping functions.

HOW TO ADD A NEW NEWS SOURCE:
----------------------------
1. Add a new entry to the NEWS_SOURCES list below
2. Each source needs:
   - id: unique identifier (lowercase, no spaces)
   - name: display name
   - base_url: main website URL
   - urls: dictionary mapping category names to their RSS/page URLs
   - color: hex color for the button (optional)

HOW TO MODIFY CATEGORIES:
------------------------
Edit the CATEGORIES list to add/remove/modify categories.
Each category needs an 'id' and 'name'.
"""

import requests
from bs4 import BeautifulSoup
import re
import random
from urllib.parse import urljoin, urlparse

NEWS_SOURCES = [
    {
        'id': 'bbc',
        'name': 'BBC',
        'base_url': 'https://www.bbc.com',
        'color': '#BB1919',
        'urls': {
            'top': 'https://www.bbc.com/news',
            'politics': 'https://www.bbc.com/news/politics',
            'sports': 'https://www.bbc.com/sport',
            'tech': 'https://www.bbc.com/news/technology',
            'international': 'https://www.bbc.com/news/world',
            'random': 'https://www.bbc.com/news'
        }
    },
    {
        'id': 'bbc_india',
        'name': 'BBC India',
        'base_url': 'https://www.bbc.com',
        'color': '#BB1919',
        'urls': {
            'top': 'https://www.bbc.com/news/world/asia/india',
            'politics': 'https://www.bbc.com/news/world/asia/india',
            'sports': 'https://www.bbc.com/sport/cricket',
            'tech': 'https://www.bbc.com/news/technology',
            'international': 'https://www.bbc.com/news/world/asia/india',
            'random': 'https://www.bbc.com/news/world/asia/india'
        }
    },
    {
        'id': 'toi',
        'name': 'Times of India',
        'base_url': 'https://timesofindia.indiatimes.com',
        'color': '#E31837',
        'urls': {
            'top': 'https://timesofindia.indiatimes.com/news',
            'politics': 'https://timesofindia.indiatimes.com/india',
            'sports': 'https://timesofindia.indiatimes.com/sports',
            'tech': 'https://timesofindia.indiatimes.com/technology',
            'international': 'https://timesofindia.indiatimes.com/world',
            'random': 'https://timesofindia.indiatimes.com'
        }
    },
    {
        'id': 'aajtak',
        'name': 'Aaj Tak',
        'base_url': 'https://www.aajtak.in',
        'color': '#E50914',
        'urls': {
            'top': 'https://www.aajtak.in/india',
            'politics': 'https://www.aajtak.in/india',
            'sports': 'https://www.aajtak.in/sports',
            'tech': 'https://www.aajtak.in/technology',
            'international': 'https://www.aajtak.in/world',
            'random': 'https://www.aajtak.in'
        }
    },
    {
        'id': 'ani',
        'name': 'ANI',
        'base_url': 'https://www.aninews.in',
        'color': '#1E3A8A',
        'urls': {
            'top': 'https://www.aninews.in',
            'politics': 'https://www.aninews.in/topic/politics',
            'sports': 'https://www.aninews.in/topic/sports',
            'tech': 'https://www.aninews.in/topic/technology',
            'international': 'https://www.aninews.in/topic/world',
            'random': 'https://www.aninews.in'
        }
    },
    {
        'id': 'cnn',
        'name': 'CNN',
        'base_url': 'https://www.cnn.com',
        'color': '#CC0000',
        'urls': {
            'top': 'https://www.cnn.com',
            'politics': 'https://www.cnn.com/politics',
            'sports': 'https://www.cnn.com/sport',
            'tech': 'https://www.cnn.com/business/tech',
            'international': 'https://www.cnn.com/world',
            'random': 'https://www.cnn.com'
        }
    },
    {
        'id': 'ndtv',
        'name': 'NDTV',
        'base_url': 'https://www.ndtv.com',
        'color': '#E31E24',
        'urls': {
            'top': 'https://www.ndtv.com/latest',
            'politics': 'https://www.ndtv.com/latest',
            'sports': 'https://www.ndtv.com/latest',
            'tech': 'https://www.ndtv.com/latest',
            'international': 'https://www.ndtv.com/latest',
            'random': 'https://www.ndtv.com/latest'
        }
    },
    {
        'id': 'indiatoday',
        'name': 'India Today',
        'base_url': 'https://www.indiatoday.in',
        'color': '#E31E24',
        'urls': {
            'top': 'https://www.indiatoday.in',
            'politics': 'https://www.indiatoday.in/india',
            'sports': 'https://www.indiatoday.in/sports',
            'tech': 'https://www.indiatoday.in/technology',
            'international': 'https://www.indiatoday.in/world',
            'random': 'https://www.indiatoday.in'
        }
    },
    {
        'id': 'abpnews',
        'name': 'ABP News',
        'base_url': 'https://news.abplive.com',
        'color': '#ED1C24',
        'urls': {
            'top': 'https://news.abplive.com',
            'politics': 'https://news.abplive.com/india',
            'sports': 'https://news.abplive.com/sports',
            'tech': 'https://news.abplive.com/technology',
            'international': 'https://news.abplive.com/world',
            'random': 'https://news.abplive.com'
        }
    },
    {
        'id': 'aljazeera',
        'name': 'Al Jazeera',
        'base_url': 'https://www.aljazeera.com',
        'color': '#D2691E',
        'urls': {
            'top': 'https://www.aljazeera.com/news',
            'politics': 'https://www.aljazeera.com/news',
            'sports': 'https://www.aljazeera.com/sports',
            'tech': 'https://www.aljazeera.com/economy',
            'international': 'https://www.aljazeera.com/news',
            'random': 'https://www.aljazeera.com'
        }
    }
]

CATEGORIES = [
    {'id': 'random', 'name': 'Generate News', 'icon': '🔄'},
    {'id': 'top', 'name': 'Top News', 'icon': '📰'},
    {'id': 'politics', 'name': 'Politics', 'icon': '🏛️'},
    {'id': 'sports', 'name': 'Sports', 'icon': '⚽'},
    {'id': 'tech', 'name': 'Tech', 'icon': '💻'},
    {'id': 'international', 'name': 'International', 'icon': '🌍'}
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
}

def clean_text(text):
    """Clean and normalize text content"""
    if not text:
        return ''
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def get_absolute_url(base_url, relative_url):
    """Convert relative URL to absolute URL"""
    if not relative_url:
        return None
    if relative_url.startswith('//'):
        return 'https:' + relative_url
    if relative_url.startswith('http'):
        return relative_url
    return urljoin(base_url, relative_url)

def is_valid_image_url(url):
    """Check if URL looks like a valid image"""
    if not url:
        return False
    url_lower = url.lower()
    invalid_patterns = ['placeholder', 'logo', 'icon', 'avatar', '1x1', 'blank', 'spacer', 
                        'grey-placeholder', 'loading', 'spinner', 'pixel', 'tracking',
                        'transparent', 'default', 'fallback', 'dummy', 'empty']
    if any(x in url_lower for x in invalid_patterns):
        return False
    if any(ext in url_lower for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']):
        return True
    if 'image' in url_lower or 'img' in url_lower or 'photo' in url_lower:
        return True
    return True

def extract_image_from_element(element, base_url):
    """Extract image URL from an element using multiple strategies"""
    if not element:
        return None
    
    img_attrs = ['src', 'data-src', 'data-original', 'data-lazy-src', 'data-srcset', 
                 'srcset', 'data-image', 'data-bg', 'data-lazyload']
    
    img = element.find('img')
    if img:
        for attr in img_attrs:
            url = img.get(attr)
            if url:
                if 'srcset' in attr.lower():
                    urls = url.split(',')
                    if urls:
                        url = urls[0].strip().split()[0]
                url = get_absolute_url(base_url, url)
                if is_valid_image_url(url):
                    return url
    
    picture = element.find('picture')
    if picture:
        source = picture.find('source')
        if source:
            srcset = source.get('srcset')
            if srcset:
                url = srcset.split(',')[0].strip().split()[0]
                url = get_absolute_url(base_url, url)
                if is_valid_image_url(url):
                    return url
    
    for tag in element.find_all(['div', 'figure', 'span', 'a']):
        style = tag.get('style', '')
        if 'background' in style:
            match = re.search(r'url\(["\']?([^"\'()]+)["\']?\)', style)
            if match:
                url = get_absolute_url(base_url, match.group(1))
                if is_valid_image_url(url):
                    return url
        
        for attr in ['data-bg', 'data-background', 'data-image']:
            url = tag.get(attr)
            if url:
                url = get_absolute_url(base_url, url)
                if is_valid_image_url(url):
                    return url
    
    return None

def extract_og_image(soup, base_url):
    """Extract Open Graph image from page meta tags"""
    og_image = soup.find('meta', property='og:image')
    if og_image:
        url = og_image.get('content')
        if url:
            return get_absolute_url(base_url, url)
    
    twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
    if twitter_image:
        url = twitter_image.get('content')
        if url:
            return get_absolute_url(base_url, url)
    
    return None

def get_session_with_referer(base_url):
    """Create a session with appropriate referer headers for difficult sites"""
    session = requests.Session()
    session.headers.update(HEADERS)
    session.headers['Referer'] = 'https://www.google.com/'
    return session

def scrape_ndtv(url, base_url):
    """Specialized scraper for NDTV using Google News RSS"""
    try:
        rss_url = 'https://feeds.feedburner.com/ndtvnews-latest'
        response = requests.get(rss_url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'xml')
        
        items = soup.find_all('item')
        if not items:
            return None
        
        articles = []
        for item in items[:15]:
            title = item.find('title')
            link = item.find('link')
            description = item.find('description')
            
            if title and link:
                headline = clean_text(title.get_text())
                article_url = link.get_text().strip()
                desc_text = clean_text(description.get_text()) if description else ''
                
                media_content = item.find('media:content') or item.find('media:thumbnail')
                image_url = None
                if media_content and media_content.get('url'):
                    image_url = media_content.get('url')
                
                enclosure = item.find('enclosure')
                if not image_url and enclosure and enclosure.get('url'):
                    image_url = enclosure.get('url')
                
                if headline and len(headline) > 20:
                    articles.append({
                        'headline': headline,
                        'description': desc_text[:200] if desc_text else '',
                        'image_url': image_url,
                        'article_url': article_url
                    })
        
        if articles:
            articles_with_images = [a for a in articles if a.get('image_url')]
            if articles_with_images:
                selected = random.choice(articles_with_images[:10])
            else:
                selected = random.choice(articles[:10])
            
            if selected and not selected.get('image_url') and selected.get('article_url'):
                try:
                    session = get_session_with_referer(base_url)
                    article_response = session.get(selected['article_url'], timeout=10)
                    if article_response.status_code == 200:
                        article_soup = BeautifulSoup(article_response.content, 'lxml')
                        og_image = extract_og_image(article_soup, base_url)
                        if og_image:
                            selected['image_url'] = og_image
                except Exception:
                    pass
            
            return selected
        return None
    except Exception as e:
        print(f"Error scraping NDTV RSS: {e}")
        return None

def scrape_toi(url, base_url):
    """Specialized scraper for Times of India"""
    try:
        session = get_session_with_referer(base_url)
        response = session.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        
        og_image = extract_og_image(soup, base_url)
        
        toi_selectors = [
            '.list_item',
            '.story-card',
            '.col_l_6',
            '.col_l_12',
            '[class*="TopStory"]',
            '.iN5CR',
            'li[data-vr-zone]',
            '.card',
            'article',
        ]
        
        articles = []
        for selector in toi_selectors:
            items = soup.select(selector)
            for item in items:
                headline_elem = item.find(['h2', 'h3', 'h1'])
                if not headline_elem:
                    link = item.find('a')
                    if link and len(clean_text(link.get_text())) > 20:
                        headline_elem = link
                
                if not headline_elem:
                    continue
                
                headline = clean_text(headline_elem.get_text())
                if not headline or len(headline) < 20 or len(headline) > 300:
                    continue
                
                if any(x in headline.lower() for x in ['subscribe', 'sign up', 'newsletter', 'cookie', 'privacy', 'download app']):
                    continue
                
                link_elem = headline_elem if headline_elem.name == 'a' else item.find('a')
                article_url = link_elem.get('href') if link_elem else None
                article_url = get_absolute_url(base_url, article_url)
                
                image_url = extract_image_from_element(item, base_url)
                
                desc_elem = item.find('p')
                description = clean_text(desc_elem.get_text()) if desc_elem else ''
                
                articles.append({
                    'headline': headline,
                    'description': description[:200] if description else '',
                    'image_url': image_url,
                    'article_url': article_url
                })
        
        seen = set()
        unique = []
        for a in articles:
            key = a['headline'][:50].lower()
            if key not in seen:
                seen.add(key)
                unique.append(a)
        
        if unique:
            with_images = [a for a in unique if a.get('image_url')]
            if with_images:
                selected = random.choice(with_images[:10])
            else:
                selected = random.choice(unique[:10])
                if not selected.get('image_url') and og_image:
                    selected['image_url'] = og_image
            
            if selected and not selected.get('image_url') and selected.get('article_url'):
                try:
                    article_response = session.get(selected['article_url'], timeout=10)
                    if article_response.status_code == 200:
                        article_soup = BeautifulSoup(article_response.content, 'lxml')
                        img = extract_og_image(article_soup, base_url)
                        if img:
                            selected['image_url'] = img
                except Exception:
                    pass
            
            return selected
        return None
    except Exception as e:
        print(f"Error scraping TOI: {e}")
        return None

def scrape_universal(url, base_url):
    """Universal news scraper that works across multiple sites"""
    try:
        session = get_session_with_referer(base_url)
        response = session.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        
        og_image = extract_og_image(soup, base_url)
        
        article_selectors = [
            'article',
            '[data-testid*="card"]',
            '[data-testid*="promo"]',
            '[class*="story-card"]',
            '[class*="news-card"]',
            '[class*="article-card"]',
            '.news-item',
            '.story',
            '.card',
            '[class*="headline"]',
            'li[class*="news"]',
            'li[class*="story"]',
            'div[class*="news"]',
            'div[class*="story"]',
        ]
        
        all_articles = []
        for selector in article_selectors:
            articles = soup.select(selector)
            for article in articles:
                headline_elem = (article.find('h2') or article.find('h3') or 
                               article.find('h1') or article.find('a', class_=re.compile(r'title|headline', re.I)))
                
                if not headline_elem:
                    link = article.find('a')
                    if link and len(clean_text(link.get_text())) > 20:
                        headline_elem = link
                
                if not headline_elem:
                    continue
                    
                headline = clean_text(headline_elem.get_text())
                
                if not headline or len(headline) < 20 or len(headline) > 300:
                    continue
                
                if any(x in headline.lower() for x in ['subscribe', 'sign up', 'newsletter', 'cookie', 'privacy']):
                    continue
                
                link_elem = headline_elem if headline_elem.name == 'a' else article.find('a')
                article_url = link_elem.get('href') if link_elem else None
                article_url = get_absolute_url(base_url, article_url)
                
                image_url = extract_image_from_element(article, base_url)
                
                if not image_url:
                    parent = article.find_parent(['article', 'div', 'section'])
                    if parent:
                        image_url = extract_image_from_element(parent, base_url)
                
                description = ''
                desc_elem = article.find('p')
                if desc_elem:
                    description = clean_text(desc_elem.get_text())
                    if len(description) < 10:
                        description = ''
                
                all_articles.append({
                    'headline': headline,
                    'description': description,
                    'image_url': image_url,
                    'article_url': article_url
                })
        
        unique_articles = []
        seen_headlines = set()
        for art in all_articles:
            headline_key = art['headline'][:50].lower()
            if headline_key not in seen_headlines:
                seen_headlines.add(headline_key)
                unique_articles.append(art)
        
        if unique_articles:
            articles_with_images = [a for a in unique_articles if a['image_url']]
            if articles_with_images:
                selected = random.choice(articles_with_images[:10])
            else:
                selected = random.choice(unique_articles[:10])
                if not selected['image_url'] and og_image:
                    selected['image_url'] = og_image
            return selected
        
        return None
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def scrape_with_article_fetch(url, base_url):
    """Scrape news list and optionally fetch article page for image"""
    result = scrape_universal(url, base_url)
    
    if result and not result.get('image_url') and result.get('article_url'):
        try:
            session = get_session_with_referer(base_url)
            article_response = session.get(result['article_url'], timeout=10)
            article_response.raise_for_status()
            article_soup = BeautifulSoup(article_response.content, 'lxml')
            
            og_image = extract_og_image(article_soup, base_url)
            if og_image:
                result['image_url'] = og_image
            else:
                main_content = (article_soup.find('article') or 
                              article_soup.find('[class*="content"]') or
                              article_soup.find('main'))
                if main_content:
                    img_url = extract_image_from_element(main_content, base_url)
                    if img_url:
                        result['image_url'] = img_url
            
            if not result.get('description'):
                first_p = article_soup.find('article')
                if first_p:
                    p = first_p.find('p')
                    if p:
                        result['description'] = clean_text(p.get_text())[:200]
        except Exception as e:
            print(f"Could not fetch article page: {e}")
    
    return result

def scrape_article(source, category='top'):
    """
    Main scraping function - routes to appropriate scraper based on source.
    
    Args:
        source: Source configuration dict from NEWS_SOURCES
        category: Category ID (top, politics, sports, tech, international, random)
    
    Returns:
        Dict with headline, description, image_url, article_url
        or None if scraping failed
    """
    base_url = source['base_url']
    source_id = source['id']
    
    if category == 'random':
        category = random.choice(['top', 'politics', 'sports', 'tech', 'international'])
    
    url = source['urls'].get(category, source['urls']['top'])
    
    if source_id == 'ndtv':
        result = scrape_ndtv(url, base_url)
        if result:
            return result
    
    if source_id == 'toi':
        result = scrape_toi(url, base_url)
        if result:
            return result
    
    result = scrape_with_article_fetch(url, base_url)
    
    if not result:
        result = scrape_universal(url, base_url)
    
    return result
