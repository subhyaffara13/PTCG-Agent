
def test_chunksize_is_incremental():
    # See https://github.com/pandas-dev/pandas/issues/34548
    jsonl = (
        """{"a": 1, "b": 2}
        {"a": 3, "b": 4}
        {"a": 5, "b": 6}
        {"a": 7, "b": 8}\n"""
        * 1000
    )

    class MyReader:
        def __init__(self, contents) -> None:
            self.read_count = 0
            self.stringio = StringIO(contents)

        def read(self, *args):
            self.read_count += 1
            return self.stringio.read(*args)

        def __iter__(self) -> Iterator:
            self.read_count += 1
            return iter(self.stringio)

    reader = MyReader(jsonl)
    assert len(list(read_json(reader, lines=True, chunksize=100))) > 1
    assert reader.read_count > 10

