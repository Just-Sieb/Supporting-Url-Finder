import unittest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .test_url_parser import TestUrlParser

if __name__ == '__main__':
    unittest.main()
