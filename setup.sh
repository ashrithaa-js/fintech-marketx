#!/bin/bash
echo "Setting up environment..."

pip install -r requirements.txt

echo "Downloading NLTK data..."
python3 - <<EOF
import nltk
nltk.download('punkt')
nltk.download('vader_lexicon')
EOF

echo "Setup complete."
