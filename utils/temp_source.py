
def temp_source(text: str) -> Iterator[str]:
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = os.path.join(temp_dir, "t.py")
        with open(temp_path, "w") as f:
            f.write(text)
        yield temp_path

