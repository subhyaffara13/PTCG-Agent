
def _ok_to_generate_guards_fn():
    patterns = [
        "executorch",
        "modai",
        "on_device_ai",
        "torchao",
    ]
    # force check_guards=False for files matching `patterns`
    # because they have too many calls to .module() and
    # do not like any call modules in the graph
    # TODO: fix these files to handle guard fns
    frame = inspect.currentframe()
    while frame is not None:
        if any(path in frame.f_code.co_filename for path in patterns):
            return False
        frame = frame.f_back

    return True

