import subprocess
import sys
import unittest

import coverage

cov = coverage.coverage()
cov.start()

from flatdoc import flatdoc


class FlatdocTestCase(unittest.TestCase):
    def test_flatdoc(self):
        self.assertEqual(flatdoc('test_data'), '''test_data
mod1
Class
method1
method2
mod2

func
method3

submod1
submod2

''')

    def test_errors(self):
        # no docstring
        self.assertRaises(ValueError, flatdoc, 'test_data.mod3')
        self.assertRaises(ValueError, flatdoc, 'test_data.mod4')

        # include cannot end in dot
        self.assertRaises(ValueError, flatdoc, 'test_data.mod5')

        # cannot reach above start module
        self.assertRaises(ValueError, flatdoc, 'test_data.mod6')

        # unknown member of class
        self.assertRaises(ValueError, flatdoc, 'test_data.mod7')

        # unknwon import
        self.assertRaises(ImportError, flatdoc, 'test_data.mod8')

if __name__ == '__main__':
    tests_ok = unittest.main(verbosity=2, exit=False).result.wasSuccessful()

    # print coverage report
    cov.stop()
    print('')
    cov.report(omit=['test_*', 'venv/*'])

    # lint the code
    print('')
    lint_ok = subprocess.call(['flake8', '--ignore=E402', 'flatdoc.py',
                               'test_flatdoc.py']) == 0

    # exit code (1: tests failed, 2: lint failed, 3: both failed)
    sys.exit((0 if tests_ok else 1) + (0 if lint_ok else 2))
