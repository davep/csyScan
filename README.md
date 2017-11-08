csyScan is a simple Python script for scanning a set of Clipper sources and
producing a simple tree to show the class hierarchy. The method used isn't
very clever, the output isn't very pretty, but it does the job. I tend to
use it to produce quick and dirty documentation.

Obviously, to use the script, you'll need a copy of Python, you will find
DOS and Windows versions of Python on the Python homepage.

A word of warning. I've not made any attempt to support multiple
inheritance.

csyScan can also produce simple Norton Guide source that includes the actual
class definition code behind each class name in the list. See csyNg.py for
an example of how to turn this on.

If you want to scan Xbase++ code, you can also use xbppscan.py. For it to
work, you will also need csyScan.py.
