"""
Tweet Generator Module
======================
Uses Perplexity API (or OpenAI) to generate high-engagement X (Twitter) posts.
"""

import os
from openai import OpenAI

MAX_TWEET_LENGTH = 280
MIN_TWEET_LENGTH = 250

client = None

def get_openai_client():
    """Get or create API client. Works with both OpenAI and Perplexity keys."""
    global client
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    
    if client is None:
        # Check if it's a Perplexity key
        if api_key.startswith('pplx-'):
            # Use Perplexity API endpoint
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.perplexity.ai"
            )
        else:
            # Use OpenAI API
            client = OpenAI(api_key=api_key)
    
    return client

def generate_tweet(headline, description='', source_name=''):
    """
    Generate a high-engagement tweet-style summary of a news article.
    """
    if not headline:
        return "Breaking news! Check out the latest updates."
    
    openai_client = get_openai_client()
    if not openai_client:
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

✅ Example:
Scraped: "Virat Kohli scores 102 in a crucial ODI, helping India seal series."
Output: 🔥 Virat Kohli delivers AGAIN! A superb 102 in a must-win ODI lifts India to a series win. His consistency right now is unreal 👑🇮🇳
Is this his best ODI form in years?
#ViratKohli #INDvAUS

Now rewrite this news from {source_name}:
{content_for_summary}

Generate ONLY the tweet text:"""

        # Detect which API and choose appropriate model
        api_key = os.environ.get("OPENAI_API_KEY", "")
        
        if api_key.startswith('pplx-'):
            # Use Perplexity's model (you can use Claude, GPT-4, etc.)
            model = "sonar"  # or "claude-3.5-sonnet" or "gpt-4o"
        else:
            # Use OpenAI's model
            model = "gpt-4o"
        
        response = openai_client.chat.completions.create(
            model=model,
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
            max_tokens=150,
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
        fallback = f"📰 {headline}"
        if len(fallback) > MAX_TWEET_LENGTH:
            fallback = f"📰 {headline[:MAX_TWEET_LENGTH - 6]}..."
        return fallback
