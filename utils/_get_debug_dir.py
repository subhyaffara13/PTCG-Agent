
def _get_debug_dir(root_dir: str) -> str:
    dir_name = (
        "run_"
        + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
        # use pid to avoid conflicts among ranks
        + "-pid_"
        + str(os.getpid())
    )
    return os.path.join(root_dir, dir_name)

