import copy
import os
import sys

def environment(**replacements):
    """
    In a context, patch the environment with replacements. Pass None values
    to clear the values.
    """
    saved = dict((key, os.environ[key]) for key in replacements if key in os.environ)

    # remove values that are null
    remove = (key for (key, value) in replacements.items() if value is None)
    for key in list(remove):
        os.environ.pop(key, None)
        replacements.pop(key)

    os.environ.update(replacements)

    try:
        yield saved
    finally:
        for key in replacements:
            os.environ.pop(key, None)
        os.environ.update(saved)


def environment(monkeypatch):
    monkeypatch.setattr(os, 'name', os.name)
    monkeypatch.setattr(sys, 'platform', sys.platform)
    monkeypatch.setattr(sys, 'version', sys.version)
    monkeypatch.setattr(os, 'sep', os.sep)
    monkeypatch.setattr(os.path, 'join', os.path.join)
    monkeypatch.setattr(os.path, 'isabs', os.path.isabs)
    monkeypatch.setattr(os.path, 'splitdrive', os.path.splitdrive)
    monkeypatch.setattr(sysconfig, '_config_vars', copy(sysconfig._config_vars))

