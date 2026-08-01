
def _frame_fmt(f, full_filename=False):
    i = f["line"]
    fname = f["filename"]
    if not full_filename:
        fname = fname.split("/")[-1]
    func = f["name"]
    return f"{fname}:{i}:{func}"

