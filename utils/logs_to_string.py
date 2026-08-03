import logging

def logs_to_string(module, log_option):
    """Example:
    logs_to_string("torch._inductor.compile_fx", "post_grad_graphs")
    returns the output of TORCH_LOGS="post_grad_graphs" from the
    torch._inductor.compile_fx module.
    """
    log_stream = io.StringIO()
    handler = logging.StreamHandler(stream=log_stream)

    @contextlib.contextmanager
    def tmp_redirect_logs():
        try:
            logger = torch._logging.getArtifactLogger(module, log_option)
            logger.addHandler(handler)
            yield
        finally:
            logger.removeHandler(handler)

    def ctx_manager():
        exit_stack = log_settings(log_option)
        exit_stack.enter_context(tmp_redirect_logs())
        return exit_stack

    return log_stream, ctx_manager

