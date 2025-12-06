"""
Tweet Generator Module
======================
Uses OpenAI to generate tweet-sized summaries of news articles.

TWEET LENGTH LIMIT:
------------------
The maximum tweet length is enforced here. Change MAX_TWEET_LENGTH below
to adjust the character limit (currently set to 280 characters).
"""

import os
from openai import OpenAI

MAX_TWEET_LENGTH = 280
MIN_TWEET_LENGTH = 250

client = None

def get_openai_client():
    """Get or create OpenAI client. Returns None if API key not set or invalid."""
    global client
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    if api_key.startswith('pplx-'):
        print("Warning: Perplexity API key detected. Please use an OpenAI API key instead.")
        return None
    if client is None:
        client = OpenAI(api_key=api_key)
    return client

def generate_tweet(headline, description='', source_name=''):
    """
    Generate a tweet-style summary of a news article.
    
    Args:
        headline: The article headline
        description: Optional article description/first paragraph
        source_name: Name of the news source
    
    Returns:
        Tweet text (between 250-280 characters)
    
    Note: The function enforces a hard limit of MAX_TWEET_LENGTH characters.
    If generation fails, it falls back to a truncated headline.
    """
    if not headline:
        return "Breaking news! Check out the latest updates."
    
    openai_client = get_openai_client()
    if not openai_client:
        source_credit = f" 📸 Source: {source_name}" if source_name else ""
        fallback = f"📰 {headline}{source_credit}"
        if len(fallback) > MAX_TWEET_LENGTH:
            available_length = MAX_TWEET_LENGTH - len(source_credit) - 6
            fallback = f"📰 {headline[:available_length]}...{source_credit}"
        return fallback
    
    try:
        content_for_summary = f"Headline: {headline}"
        if description:
            content_for_summary += f"\n\nDescription: {description}"
        
        prompt = f"""Create a detailed, engaging tweet-sized news summary. CRITICAL REQUIREMENTS:
1. LENGTH: The tweet MUST be between {MIN_TWEET_LENGTH} and {MAX_TWEET_LENGTH} characters. Count carefully!
2. Write in clear, engaging English with proper grammar
3. Be factual - expand on the headline with context and details from the description
4. Include 1-2 relevant hashtags
5. IMPORTANT: End the tweet with "📸 Source: {source_name}" to credit the news source
6. Make it informative, shareable and newsworthy
7. Do NOT add quotation marks around the tweet
8. Use the full character limit - short tweets are NOT acceptable

Article from {source_name}:
{content_for_summary}

Format example: "[News summary with context and details] #Hashtag1 #Hashtag2 📸 Source: {source_name}"

Remember: The tweet MUST be between {MIN_TWEET_LENGTH}-{MAX_TWEET_LENGTH} characters. Add details to reach the minimum. Always end with the source credit.

Generate ONLY the tweet text:"""

        # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
        # do not change this unless explicitly requested by the user
        response = openai_client.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a professional news editor who creates detailed, engaging tweet summaries. Your tweets MUST be between {MIN_TWEET_LENGTH}-{MAX_TWEET_LENGTH} characters - never shorter. Include context, details, and hashtags. Never exceed {MAX_TWEET_LENGTH} characters. Never hallucinate facts."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_completion_tokens=200
        )
        
        tweet = response.choices[0].message.content
        if tweet:
            tweet = tweet.strip().strip('"\'')
        else:
            raise ValueError("Empty response from API")
        
        if len(tweet) > MAX_TWEET_LENGTH:
            tweet = tweet[:MAX_TWEET_LENGTH - 3].rsplit(' ', 1)[0] + '...'
        
        return tweet
        
    except Exception as e:
        print(f"Error generating tweet: {e}")
        source_credit = f" 📸 Source: {source_name}" if source_name else ""
        fallback = f"📰 {headline}{source_credit}"
        if len(fallback) > MAX_TWEET_LENGTH:
            available_length = MAX_TWEET_LENGTH - len(source_credit) - 6
            fallback = f"📰 {headline[:available_length]}...{source_credit}"
        return fallback
