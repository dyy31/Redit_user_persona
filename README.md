#Reddit User Persona Generator (Open-Source, No LLMs)

This project builds a user persona based on a Reddit user's public activity, including their posts and comments using completely free and open-source tools (no OpenAI or paid APIs required).

It performs natural language analysis to infer:
- Likely age range
- Tone and sentiment
- Top subreddit interests
- Writing behavior and style
- Example posts/comments as citations

It performs natural language analysis to infer:
- Likely age range
- Tone and sentiment
- Top subreddit interests
- Writing behavior and style
- Example posts/comments as citations

 Installation
1. Clone the repository:
2. Install dependencies
   - pip install praw spacy nltk
   - python -m nltk.downloader vader_lexicon
   - python -m spacy download en_core_web_sm
3. Configure Reddit API
4. Run the script
