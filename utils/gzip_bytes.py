
def gzip_bytes(response_bytes):
    with BytesIO() as bio:
        with gzip.GzipFile(fileobj=bio, mode="w") as zipper:
            zipper.write(response_bytes)
        return bio.getvalue()

