
def action_dispose(args: Any) -> str:
    global cached_agent, disposed
    if disposed:
        return "Already disposed"

    cached_agent = None
    if args.log_path is not None:
        with open(args.log_path, mode="a") as log_file:
            log_file.write("]")
    disposed = True
    return "Successfully disposed"

