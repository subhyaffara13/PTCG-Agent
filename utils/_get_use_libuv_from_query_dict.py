
def _get_use_libuv_from_query_dict(query_dict: dict[str, str]) -> bool:
    # libuv is the default backend for TCPStore. To enable the non-libuv backend,
    # user can explicitly specify ``use_libuv=0`` in the URL parameter.
    if sys.platform == "win32":
        #  PyTorch is built without libuv support on windows, so default to 0
        return query_dict.get("use_libuv", os.environ.get("USE_LIBUV", "0")) == "1"
    return query_dict.get("use_libuv", os.environ.get("USE_LIBUV", "1")) == "1"

