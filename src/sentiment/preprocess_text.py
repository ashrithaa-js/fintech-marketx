import nltk
from nltk.tokenize import word_tokenize

# Ensure necessary NLTK tokenizers are available
for resource in ["punkt", "punkt_tab"]:
    try:
        nltk.data.find(f"tokenizers/{resource}")
    except LookupError:
        print(f"⚠ '{resource}' not found. Downloading now...")
        nltk.download(resource)

def clean_text(text):
    tokens = word_tokenize(text.lower())
    return " ".join(tokens)
