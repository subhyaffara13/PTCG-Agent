
def torch_key() -> bytes:
    """
    Compute a key that contains relevant information about torch source files
    """
    with dynamo_timed("inductor_codecache_torch_key", log_pt2_compile_event=False):
        if not config.is_fbcode():

            def get_code_hash(root: str) -> bytes:
                # This function isn't meant to be used outside of torch_key, just a
                # helper for clarity. Instead, use torch_key() directly when you need
                # a hash representing the state of the source code.
                extra_files = (
                    "codegen/aoti_runtime/interface.cpp",
                    "script.ld",
                )
                inductor_root = os.path.dirname(__file__)
                extra_files = [os.path.join(inductor_root, x) for x in extra_files]
                hasher = hashlib.sha256()
                hasher.update(torch.__version__.encode("utf-8"))
                build_code_hash([root], "", hasher)
                for path in extra_files:
                    if os.path.exists(path):
                        with open(path, "rb") as f:
                            hasher.update(f.read())
                return hasher.digest()

            return get_code_hash(_TORCH_PATH)

        from libfb.py import parutil

        return parutil.get_file_contents("torch/src_hash.txt").rstrip().encode("ascii")

