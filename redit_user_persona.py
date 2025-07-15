import praw
import re
import nltk
import spacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
from datetime import datetime

#SETUP
REDDIT_CLIENT_ID = 'Krb7stFg9GL2J5-6Wg7F3g'
REDDIT_CLIENT_SECRET = 'ldshW5ww2fCUUfbIaQUIJy8oA5FRyw'
REDDIT_USER_AGENT = 'script:RedditPersonaApp:v1.0 (by u/Calm-Celebration9041)'

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()
nlp = spacy.load('en_core_web_sm')

#FUNCTIONS

def extract_username(url):
    match = re.match(r'https?://www\.reddit\.com/user/([^/]+)/?', url)
    return match.group(1) if match else None

def fetch_data(username, limit=100):
    user = reddit.redditor(username)
    posts, comments = [], []
    try:
        for p in user.submissions.new(limit=limit):
            posts.append({
                "text": p.title + " " + p.selftext,
                "subreddit": str(p.subreddit),
                "url": f"https://reddit.com{p.permalink}"
            })
    except:
        pass
    try:
        for c in user.comments.new(limit=limit):
            comments.append({
                "text": c.body,
                "subreddit": str(c.subreddit),
                "url": f"https://reddit.com{c.permalink}"
            })
    except:
        pass
    return posts, comments

def analyze_text(texts):
    all_text = " ".join([t['text'] for t in texts])
    doc = nlp(all_text)
    word_count = len([t for t in doc if t.is_alpha])
    pronouns = [token.text.lower() for token in doc if token.pos_ == "PRON"]
    personal_pronoun_ratio = pronouns.count("i") / (len(pronouns) + 1)
    return word_count, personal_pronoun_ratio

def analyze_sentiment(texts):
    scores = [sid.polarity_scores(t['text'])['compound'] for t in texts]
    avg_score = sum(scores) / len(scores) if scores else 0
    if avg_score > 0.3:
        return "Positive"
    elif avg_score < -0.3:
        return "Negative"
    else:
        return "Neutral"

def top_interests(posts, comments):
    subs = [p['subreddit'] for p in posts + comments]
    return [s for s, _ in Counter(subs).most_common(3)]

def generate_persona(username, posts, comments):
    all_texts = posts + comments
    word_count, pronoun_ratio = analyze_text(all_texts)
    tone = analyze_sentiment(all_texts)
    interests = top_interests(posts, comments)

    age_guess = "18–24" if pronoun_ratio > 0.5 else "25–34"
    behavior = "Engages frequently" if word_count > 2000 else "Occasional contributor"

    lines = [
        f"User Persona for u/{username}",
        "-----------------------------------------",
        f"Fictional Name: Redditor_{username.capitalize()}",
        f"Age Range: {age_guess} (based on pronoun usage)",
        f"Tone: {tone}",
        f"Subreddit Interests: {', '.join(interests)}",
        f"Posting Behavior: {behavior}",
        f"Likely Personality: {'Casual and expressive' if tone == 'Positive' else 'Reserved or critical'}",
        "",
        "Citations (sample posts/comments):"
    ]

    for t in all_texts[:5]:
        lines.append(f"- {t['text'][:100].strip()}... [Link: {t['url']}]")

    return "\n".join(lines)

def save_to_file(username, content):
    filename = f"{username}_persona.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Persona saved to {filename}")

# MAIN EXECUTION
if __name__ == "__main__":
    url = input("Enter Reddit user profile URL: ").strip()
    username = extract_username(url)

    if not username:
        print("Invalid Reddit URL.")
    else:
        posts, comments = fetch_data(username)
        if not posts and not comments:
            print("No content found.")
        else:
            persona = generate_persona(username, posts, comments)
            save_to_file(username, persona)
