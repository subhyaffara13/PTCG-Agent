
def fake_open(all_contents):
    def open(path):
        contents = all_contents.get(path)
        if contents is None:
            raise FileNotFoundError(path)
        return StringIO(contents)
    return open

