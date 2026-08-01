
def action_handler(args: Any) -> str | dict[str, Any]:
    try:
        if args.action == "list":
            return action_list(args)
        if args.action == "http-server":
            return {"error": "Already running a http server."}
        if args.action == "act":
            return action_act(args)
        if args.action == "dispose":
            return action_dispose(args)
        if args.action == "load":
            return action_load(args)

        if args.environment is None:
            return {"error": "Environment required."}

        if args.action == "evaluate":
            return action_evaluate(args)
        if args.action == "step":
            return action_step(args)
        if args.action == "run":
            return action_run(args)

        return {"error": "Unknown Action"}
    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()}

