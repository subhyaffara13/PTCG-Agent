
def _jupyter_abspath(subcommand: str) -> str:
    """This method get the abspath of a specified jupyter-subcommand with no
    changes on ENV.
    """
    # get env PATH with self
    search_path = os.pathsep.join(_path_with_self())
    # get the abs path for the jupyter-<subcommand>
    jupyter_subcommand = f"jupyter-{subcommand}"
    abs_path = which(jupyter_subcommand, path=search_path)
    if abs_path is None:
        msg = f"\nJupyter command `{jupyter_subcommand}` not found."
        raise Exception(msg)

    if not os.access(abs_path, os.X_OK):
        msg = f"\nJupyter command `{jupyter_subcommand}` is not executable."
        raise Exception(msg)

    return abs_path

