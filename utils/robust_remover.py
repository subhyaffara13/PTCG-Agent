
def robust_remover():
    return (
        functools.partial(shutil.rmtree, onerror=remove_readonly)
        if platform.system() == 'Windows'
        else shutil.rmtree
    )

