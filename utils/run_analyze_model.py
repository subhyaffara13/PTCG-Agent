import logging

def run_analyze_model():
    args = parse_args()
    logger = logging.getLogger("default")

    if args.log_level == "debug":
        logger.setLevel(logging.DEBUG)
    elif args.log_level == "info":
        logger.setLevel(logging.INFO)
    elif args.log_level == "warning":
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.ERROR)

    model_path = args.model_path.resolve()
    analyze_model(model_path, args.skip_optimize, logger)

