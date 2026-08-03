import os

def test_environ():
    # See: https://github.com/pytoolz/cytoolz/issues/127
    assert keymap(identity, os.environ) == os.environ
    assert valmap(identity, os.environ) == os.environ
    assert itemmap(identity, os.environ) == os.environ

