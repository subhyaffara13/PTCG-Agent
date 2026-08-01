
def test_get_abi_tag_windows(monkeypatch):
    monkeypatch.setattr(tags, "interpreter_name", lambda: "cp")
    monkeypatch.setattr(sysconfig, "get_config_var", lambda x: "cp313-win_amd64")
    assert get_abi_tag() == "cp313"
    monkeypatch.setattr(sys, "gettotalrefcount", lambda: 1, False)
    assert get_abi_tag() == "cp313d"
    monkeypatch.setattr(sysconfig, "get_config_var", lambda x: "cp313t-win_amd64")
    assert get_abi_tag() == "cp313td"
    monkeypatch.delattr(sys, "gettotalrefcount")
    assert get_abi_tag() == "cp313t"

