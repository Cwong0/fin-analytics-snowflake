import sys
from pathlib import Path

# Add the "src" directory so tests can import fin_analytics (src layout)
SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))
