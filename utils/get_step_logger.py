
def get_step_logger(logger: logging.Logger) -> Callable[..., None]:
    if not disable_progress:
        pbar.update(1)
        if not isinstance(pbar, _Faketqdm):
            pbar.set_postfix_str(f"{logger.name}")

    step = next(_step_counter)

    def log(level: int, msg: str, **kwargs: Any) -> None:
        if "stacklevel" not in kwargs:
            kwargs["stacklevel"] = 2
        logger.log(level, "Step %s: %s", step, msg, **kwargs)

    return log

