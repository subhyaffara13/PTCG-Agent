import re

def test_show_versions_console(capsys):
    # gh-32041
    # gh-32041
    pd.show_versions(as_json=False)
    result = capsys.readouterr().out

    # check header
    assert "INSTALLED VERSIONS" in result

    # check full commit hash
    assert re.search(r"commit\s*:\s[0-9a-f]{40}\n", result)

    # check required dependency
    # 2020-12-09 npdev has "dirty" in the tag
    # 2022-05-25 npdev released with RC wo/ "dirty".
    # Just ensure we match [0-9]+\..* since npdev version is variable
    assert re.search(r"numpy\s*:\s[0-9]+\..*\n", result)

    # check optional dependency
    assert re.search(r"pyarrow\s*:\s([0-9]+.*|None)\n", result)

