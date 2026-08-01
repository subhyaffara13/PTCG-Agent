
def test_markdown_options(fsspectest):
    pytest.importorskip("tabulate")
    df = DataFrame({"a": [0]})
    df.to_markdown("testmem://mockfile", storage_options={"test": "md_write"})
    assert fsspectest.test[0] == "md_write"
    assert fsspectest.cat("testmem://mockfile")

