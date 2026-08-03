import os

def teardown_module():
    urllib_request.urlopen = old_urlopen


def teardown_module():
    if os.path.exists(fname):
        os.remove(fname)

