"""
Tweet Generator Module
======================
Uses OpenAI to generate high-engagement X (Twitter) posts from news articles.

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
    Generate a high-engagement tweet-style summary of a news article.
    
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
        # Fallback without OpenAI
        fallback = f"📰 {headline}"
        if len(fallback) > MAX_TWEET_LENGTH:
            fallback = f"📰 {headline[:MAX_TWEET_LENGTH - 6]}..."
        return fallback
    
    try:
        content_for_summary = f"Headline: {headline}"
        if description:
            content_for_summary += f"\n\nDescription: {description}"
        
        prompt = f"""Rewrite the scraped news into a high-engagement X (Twitter) post following these rules:

1. Length must be {MIN_TWEET_LENGTH}–{MAX_TWEET_LENGTH} characters.
2. Begin with a relevant emotional hook connected to the actual news topic.
3. Use 1–3 emojis that fit the news context.
4. Summarize the news using only facts present in the scraped text.
5. Keep the tone conversational and impactful.
6. End with a short question that encourages replies.
7. Include scraped hashtags if present; do not invent new ones.
8. Do not add any unrelated information, assumptions, fake drama, opinions, or extra facts.
9. Output only the rewritten post—no explanations.
10. Do NOT wrap the output in quotation marks.

✅ Example of How It Would Transform:

Scraped news:
"Virat Kohli scores 102 in a crucial ODI, helping India seal series."

Output:
🔥 Virat Kohli delivers AGAIN! A superb 102 in a must-win ODI lifts India to a series win. His consistency right now is unreal 👑🇮🇳
Is this his best ODI form in years?
#ViratKohli #INDvAUS

Now rewrite this news from {source_name}:
{content_for_summary}

Generate ONLY the tweet text:"""

        # the newest OpenAI model is "gpt-4o" (as of Dec 2024)
        # Change to "gpt-4-turbo" or "gpt-3.5-turbo" if you don't have access
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": f"You are an expert X (Twitter) content creator who rewrites news into viral, high-engagement posts. Your tweets MUST be between {MIN_TWEET_LENGTH}-{MAX_TWEET_LENGTH} characters. Use emotional hooks, conversational tone, relevant emojis, and end with engaging questions. Never hallucinate facts—use only what's in the scraped content."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_completion_tokens=150,
            temperature=0.8
        )
        
        tweet = response.choices[0].message.content
        if tweet:
            tweet = tweet.strip().strip('"\'')
        else:
            raise ValueError("Empty response from API")
        
        # Enforce hard limit
        if len(tweet) > MAX_TWEET_LENGTH:
            tweet = tweet[:MAX_TWEET_LENGTH - 3].rsplit(' ', 1)[0] + '...'
        
        return tweet
        
    except Exception as e:
        print(f"Error generating tweet: {e}")
        # Simple fallback
        fallback = f"📰 {headline}"
        if len(fallback) > MAX_TWEET_LENGTH:
            fallback = f"📰 {headline[:MAX_TWEET_LENGTH - 6]}..."
        return fallback
