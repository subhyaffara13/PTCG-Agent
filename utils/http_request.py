import json
from typing import Any

def http_request(request: Any) -> tuple[str | dict[str, Any], int, dict[str, str]]:
    # Set CORS headers for the preflight request
    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }

        return "", 204, headers

    headers = {"Access-Control-Allow-Origin": "*"}
    params = request.args.to_dict()
    for key in list(params.keys()):
        if key.endswith("[]"):
            params[key.replace("[]", "")] = request.args.getlist(key)
            del params[key]
        elif key.endswith("{}"):
            params[key.replace("{}", "")] = json.loads(params[key])
            del params[key]

    body = request.get_json(silent=True, force=True) or {}
    args = {**params, **body}
    if "render" in args and isinstance(args["render"], str):
        # Manually deserialize render argument
        # We should eventually refactor this to use the same deserializer as the cmd line arg parser
        args["render"] = json.loads(args["render"])
    args = parse_args(args)
    if args.log_path is None:
        args.log_path = log_path

    global disposed
    # Write the opening array brace for the logs file if there is a logs file.
    if disposed and args["action"] != "dispose" and args.log_path is not None:
        with open(args.log_path, mode="w") as log_file:
            log_file.write("[")
        disposed = False

    resp = action_handler(args)
    return resp, 200, headers

