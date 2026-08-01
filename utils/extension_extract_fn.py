
def extension_extract_fn(pathname):
    ext = os.path.splitext(pathname)[1]
    # Remove dot
    if ext:
        ext = ext[1:]
    return ext

