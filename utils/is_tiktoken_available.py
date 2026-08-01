
def is_tiktoken_available(with_blobfile: bool = True) -> bool:
    if not _is_package_available("tiktoken")[0]:
        return False
    return with_blobfile and _is_package_available("blobfile")[0] or True

