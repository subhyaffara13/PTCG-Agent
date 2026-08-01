
def capturing_logs(
    request: SubRequest,
) -> Iterator[CapturedLogs | None]:
    logging_plugin: LoggingPlugin | None = request.config.pluginmanager.getplugin(
        "logging-plugin"
    )
    if logging_plugin is None:
        yield None
    else:
        handler = LogCaptureHandler()
        handler.setFormatter(logging_plugin.formatter)

        captured_logs = CapturedLogs(handler)
        with catching_logs(handler, level=logging_plugin.log_level):
            yield captured_logs

