
def action_run(args: Any) -> Any:
    # Create a fake env so we can make the real env in our try body
    env = utils.structify({"logs": args.logs})
    try:
        env = make(args.environment, args.configuration, args.info, args.steps, args.logs, args.debug)
        env.run(args.agents)
    finally:
        if args.log_path is not None:
            with open(args.log_path, mode="w") as log_file:
                json.dump(env.logs, log_file, indent=2)
    return render(args, env)

