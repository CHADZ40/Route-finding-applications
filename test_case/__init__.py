"""Test case: unit tests for every study_case module.

Run from the project root:  python -m unittest -v
"""

import sys
from pathlib import Path

# Make ``study_case`` importable no matter where the tests are started from.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
