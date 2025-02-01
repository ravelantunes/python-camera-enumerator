import os
import sys

# Get the directory containing conftest.py, then go one level up to include 'src'
current_dir = os.path.dirname(__file__)
src_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, src_dir)