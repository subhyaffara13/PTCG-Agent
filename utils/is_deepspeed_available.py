
def is_deepspeed_available():
    package_exists = importlib.util.find_spec("deepspeed") is not None

    # Check we're not importing a "deepspeed" directory somewhere but the actual library by trying to grab the version
    # AND checking it has an author field in the metadata that is HuggingFace.
    if package_exists:
        try:
            _ = importlib.metadata.metadata("deepspeed")
            return True
        except importlib.metadata.PackageNotFoundError:
            return False

