import os

def test_universal_deprecated(dummy_dist, monkeypatch, tmp_path):
    monkeypatch.chdir(dummy_dist)
    with pytest.warns(SetuptoolsDeprecationWarning, match=".*universal is deprecated"):
        bdist_wheel_cmd(bdist_dir=str(tmp_path), universal=True).run()

    # For now we still respect the option
    assert os.path.exists("dist/dummy_dist-1.0-py2.py3-none-any.whl")

