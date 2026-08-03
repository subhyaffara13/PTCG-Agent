from typing import Any

def action_http(args: Any) -> None:
    from flask import Flask, request

    if args.log_path is not None:
        global log_path
        log_path = args.log_path

    # Setup logging to console for Flask
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "%(levelname)s: %(message)s",
                }
            },
            "handlers": {
                "wsgi": {"class": "logging.StreamHandler", "stream": "ext://sys.stdout", "formatter": "default"}
            },
            "root": {"level": "INFO", "handlers": ["wsgi"]},
        }
    )

    app = Flask(__name__, static_url_path="", static_folder="")
    app.route("/", methods=["GET", "POST"])(lambda: http_request(request))
    app.run(args.host, args.port, debug=args.debug, use_reloader=args.debug)

