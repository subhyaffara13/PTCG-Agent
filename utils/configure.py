import logging
import sys

def configure() -> None:
    """
    Configure logging to emit warning and above to stderr
    and everything else to stdout. This behavior is provided
    for compatibility with distutils.log but may change in
    the future.
    """
    err_handler = logging.StreamHandler()
    err_handler.setLevel(logging.WARNING)
    out_handler = logging.StreamHandler(sys.stdout)
    out_handler.addFilter(_not_warning)
    handlers = err_handler, out_handler
    logging.basicConfig(
        format="{message}", style='{', handlers=handlers, level=logging.DEBUG
    )
    if inspect.ismodule(distutils.dist.log):
        monkey.patch_func(set_threshold, distutils.log, 'set_threshold')
        # For some reason `distutils.log` module is getting cached in `distutils.dist`
        # and then loaded again when patched,
        # implying: id(distutils.log) != id(distutils.dist.log).
        # Make sure the same module object is used everywhere:
        distutils.dist.log = distutils.log


def configure(handler: MetricHandler, group: str | None = None):
    if group is None:
        global _default_metrics_handler
        # pyre-fixme[9]: _default_metrics_handler has type `NullMetricHandler`; used
        #  as `MetricHandler`.
        _default_metrics_handler = handler
    else:
        _metrics_map[group] = handler


def configure(timer_client: TimerClient):
    """
    Configures a timer client. Must be called before using ``expires``.
    """
    global _timer_client
    _timer_client = timer_client
    logger.info("Timer client configured to: %s", type(_timer_client).__name__)


def configure():
    """Initialized configuration of polys module. """
    from os import getenv

    for key, default in _default_config.items():
        value = getenv('SYMPY_' + key)

        if value is not None:
            try:
                _current_config[key] = eval(value)
            except NameError:
                _current_config[key] = value
        else:
            _current_config[key] = default


def configure() -> None:
    """
    Configure logging to emit warning and above to stderr
    and everything else to stdout. This behavior is provided
    for compatibility with distutils.log but may change in
    the future.
    """
    err_handler = logging.StreamHandler()
    err_handler.setLevel(logging.WARNING)
    out_handler = logging.StreamHandler(sys.stdout)
    out_handler.addFilter(_not_warning)
    handlers = err_handler, out_handler
    logging.basicConfig(
        format="{message}", style="{", handlers=handlers, level=logging.DEBUG
    )

