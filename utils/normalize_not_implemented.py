
def normalize_not_implemented(arg, parm):  # codespell:ignore
    if arg != parm.default:  # codespell:ignore
        raise NotImplementedError(
            f"'{parm.name}' parameter is not supported."  # codespell:ignore
        )

