import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import unittest
from test_block import BlockTest
from test_page import PageTest

if __name__ == '__main__':
    unittest.main(verbosity=2)