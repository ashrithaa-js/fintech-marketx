import sys
from pathlib import Path

# Ensure project root is on sys.path so `src.*` imports work when running Streamlit
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

