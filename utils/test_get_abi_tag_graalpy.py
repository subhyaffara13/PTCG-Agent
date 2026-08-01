
def test_get_abi_tag_graalpy(monkeypatch):
    monkeypatch.setattr(
        sysconfig, "get_config_var", lambda x: "graalpy231-310-native-x86_64-linux"
    )
    monkeypatch.setattr(tags, "interpreter_name", lambda: "graalpy")
    assert get_abi_tag() == "graalpy231_310_native"

