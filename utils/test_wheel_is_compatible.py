
def test_wheel_is_compatible(monkeypatch):
    def sys_tags():
        return {
            (t.interpreter, t.abi, t.platform)
            for t in parse_tag('cp36-cp36m-manylinux1_x86_64')
        }

    monkeypatch.setattr('setuptools.wheel._get_supported_tags', sys_tags)
    assert Wheel('onnxruntime-0.1.2-cp36-cp36m-manylinux1_x86_64.whl').is_compatible()

