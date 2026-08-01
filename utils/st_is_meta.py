
def st_is_meta(types, args=(), kwargs=None, pg=None):
    # pyrefly: ignore [bad-index]
    return args[0].local_tensor().is_meta

