import unittest, tempfile, os
from . import dyetest

def global_setUp():
    dyetest.session_path = tempfile.mkdtemp(prefix="PyDye_")

def global_tearDown():
    os.system("open %s"%dyetest.session_path)    

def run():
    global_setUp()
    all_tests = unittest.TestSuite(unittest.TestLoader().discover('.'))
    unittest.TextTestRunner().run(all_tests)
    global_tearDown()
    