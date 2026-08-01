
def _wrap_submodules(f, preserve_signature, module_call_signatures):
    handles = []

    try:
        for path in preserve_signature:
            handles.extend(_wrap_submodule(f, path, module_call_signatures))
        yield
    finally:
        for handle in handles:
            handle.remove()

