
def action_load(args: Any) -> Any:
    if args.log_path is not None:
        with open(args.log_path, mode="r") as log_file:
            args.logs = json.load(log_file)

    if args.in_path is not None:
        with open(args.in_path, mode="r") as replay_file:
            json_args = json.load(replay_file)
        env = make(
            json_args["name"], json_args["configuration"], json_args["info"], json_args["steps"], args.logs, args.debug
        )
    else:
        env = make(args.environment, args.configuration, args.info, args.steps, args.logs, args.debug)
    return render(args, env)

