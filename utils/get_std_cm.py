
def get_std_cm(std_rd: str, redirect_fn):
    if IS_WINDOWS or IS_MACOS or not std_rd:
        return nullcontext()
    else:
        return redirect_fn(std_rd)

