import os

def _set_debug(ctx: click.Context, param: click.Option, value: bool) -> bool | None:
    # If the flag isn't provided, it will default to False. Don't use
    # that, let debug be set by env in that case.
    source = ctx.get_parameter_source(param.name)  # type: ignore[arg-type]

    if source is not None and source in (
        ParameterSource.DEFAULT,
        ParameterSource.DEFAULT_MAP,
    ):
        return None

    # Set with env var instead of ScriptInfo.load so that it can be
    # accessed early during a factory function.
    os.environ["FLASK_DEBUG"] = "1" if value else "0"
    return value


def _set_debug(value):
    """Enable or disable PSUTIL_DEBUG option, which prints debugging
    messages to stderr.
    """
    import psutil._common

    psutil._common.PSUTIL_DEBUG = bool(value)
    _psplatform.cext.set_debug(bool(value))

