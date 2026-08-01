
def videohandler(extension, data):
    if extension not in [
        "mp4",
        "ogv",
        "mjpeg",
        "avi",
        "mov",
        "h264",
        "mpg",
        "webm",
        "wmv",
    ]:
        return None

    try:
        import torchvision.io
    except ImportError as e:
        raise ModuleNotFoundError(
            "Package `torchvision` is required to be installed for default video file loader."
            "Please use `pip install torchvision`"
            "to install the package"
        ) from e

    with tempfile.TemporaryDirectory() as dirname:
        fname = os.path.join(dirname, f"file.{extension}")
        with open(fname, "wb") as stream:
            stream.write(data)
            return torchvision.io.read_video(fname)

