# src/tests/conftest.py
import pytest
from pathlib import Path
import sys

@pytest.fixture(autouse=True)
def add_path():
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))