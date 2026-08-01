
def latin1_fail():
    try:
        desc, filename = tempfile.mkstemp(suffix=Filenames.latin_1)
        os.close(desc)
        os.remove(filename)
    except Exception:
        return True

