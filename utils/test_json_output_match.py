
def test_json_output_match(capsys, tmpdir):
    # GH39701
    pd.show_versions(as_json=True)
    result_console = capsys.readouterr().out

    out_path = os.path.join(tmpdir, "test_json.json")
    pd.show_versions(as_json=out_path)
    with open(out_path, encoding="utf-8") as out_fd:
        result_file = out_fd.read()

    assert result_console == result_file

