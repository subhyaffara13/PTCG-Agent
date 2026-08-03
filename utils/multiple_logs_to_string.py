import logging
from typing import Callable

def multiple_logs_to_string(module: str, *log_options: str) -> tuple[list[io.StringIO], Callable[[], AbstractContextManager[None]]]:
    """Example:
    multiple_logs_to_string("torch._inductor.compile_fx", "pre_grad_graphs", "post_grad_graphs")
    returns the output of TORCH_LOGS="pre_graph_graphs, post_grad_graphs" from the
    torch._inductor.compile_fx module.
    """
    log_streams = [io.StringIO() for _ in range(len(log_options))]
    handlers = [logging.StreamHandler(stream=log_stream) for log_stream in log_streams]

    @contextlib.contextmanager
    def tmp_redirect_logs():
        loggers = [torch._logging.getArtifactLogger(module, option) for option in log_options]
        try:
            for logger, handler in zip(loggers, handlers, strict=True):
                logger.addHandler(handler)
            yield
        finally:
            for logger, handler in zip(loggers, handlers, strict=True):
                logger.removeHandler(handler)

    def ctx_manager() -> AbstractContextManager[None]:
        exit_stack = log_settings(", ".join(log_options))
        exit_stack.enter_context(tmp_redirect_logs())
        return exit_stack  # type: ignore[return-value]

    return log_streams, ctx_manager

