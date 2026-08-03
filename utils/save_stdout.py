import sys

def save_stdout(monkeypatch):
    monkeypatch.setattr(sys, 'stdout', sys.stdout)

