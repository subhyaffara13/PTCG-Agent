import os
import re

def has_stable_flags(testcase: DataDrivenTestCase) -> bool:
    if any(re.match(r"# flags[2-9]:", line) for line in testcase.input):
        return False
    for filename, contents in testcase.files:
        if os.path.basename(filename).startswith("mypy.ini."):
            return False
    return True

