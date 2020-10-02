"""Check that the Python version is at least up to a minimum threshold of 3.6.

The instructions explicitly invoke each command using `python3` on the command
line, but a student's local setup might not default to using Python 3.6+, which
is required for this project. Additionally, some students may accidentally be in
the habit of using bare `python`, which could invoke Python 2.x if their
environment isn't set up correctly.

Other modules in this project aggressively assume Python 3.6+, so this unit test
is our only cession to the possibility that students might be running a lower
version of Python.

To run these tests from the project root, run:

    $ python3 -m unittest --verbose tests.test_python_version

These tests should (successfully) fail, but not crash, when invoked with Python 2:

    $ /usr/bin/python2.7 -m unittest --verbose tests.test_python_version

"""
import sys
import unittest


class TestPythonVersion(unittest.TestCase):
    """Check that the Python version is >= 3.6."""

    def test_python_version_is_at_least_3_6(self):
        self.assertTrue(sys.version_info >= (3, 6),
                        msg="""Unsupported Python version.

    It looks like you're using a version of Python that's too old.
    This project requires Python 3.6+. You're currently using Python {}.{}.{}.

    Make sure that you have a compatible version of Python and that you're using
    `python3` at the command-line (or that your environment resolves `python` to
    some Python3.6+ version if you have a custom setup).

    Remember, you can always ask Python to display its version with:

        $ python3 -V
        Python 3.X.Y

    """.format(*sys.version_info[:3]))


if __name__ == '__main__':
    unittest.main()
