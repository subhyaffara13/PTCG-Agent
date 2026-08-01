
def makedist(path, **attrs):
    return Distribution({"src_root": path, **attrs})

