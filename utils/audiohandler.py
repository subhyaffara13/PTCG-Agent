
def audiohandler(extension, data):
    if extension not in ["flac", "mp3", "sox", "wav", "m4a", "ogg", "wma"]:
        return None

    try:
        import torchaudio  # type: ignore[import]
    except ImportError as e:
        raise ModuleNotFoundError(
            "Package `torchaudio` is required to be installed for default audio file loader."
            "Please use `pip install torchaudio`"
            "to install the package"
        ) from e

    with tempfile.TemporaryDirectory() as dirname:
        fname = os.path.join(dirname, f"file.{extension}")
        with open(fname, "wb") as stream:
            stream.write(data)
            return torchaudio.load(fname)

