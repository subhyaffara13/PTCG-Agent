
def _newer(source, target):
    return not os.path.exists(target) or (
        os.path.getmtime(source) > os.path.getmtime(target)
    )

