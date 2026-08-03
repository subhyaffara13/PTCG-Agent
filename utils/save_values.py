import sys

def save_values(monkeypatch):
    monkeypatch.setattr(sys, 'platform', sys.platform)
    monkeypatch.setattr(sysconfig, 'get_config_var', sysconfig.get_config_var)
    monkeypatch.setattr(sysconfig, 'get_config_vars', sysconfig.get_config_vars)

