"""Tools for developing machine-learning models based a dataset from LendingClub.

The modules in this package are developed to simplify the code in Jupyter notebooks.
Access to the package from within notebooks is facilitated by installing it in the
virtual environment used to run Jupyter Server, e.g., by executing the command
    poetry install
"""
from pathlib import Path

ROOT_DIR = Path(__file__).parent
DATA_DIR = ROOT_DIR.parent / "data"
