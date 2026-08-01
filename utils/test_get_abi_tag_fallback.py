
def test_get_abi_tag_fallback(monkeypatch):
    monkeypatch.setattr(sysconfig, "get_config_var", lambda x: "unknown-python-310")
    monkeypatch.setattr(tags, "interpreter_name", lambda: "unknown-python")
    assert get_abi_tag() == "unknown_python_310"

