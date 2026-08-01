
def print_args(args):
    for arg in vars(args):
        logger.info(f"{arg}: {getattr(args, arg)}")

