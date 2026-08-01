
def init_verbose_loggers():
    try:
        worker_config = get_secret_str("WORKER_CONFIG")
        # if not, assume it's a json string
        if worker_config is None:
            return
        if os.path.isfile(worker_config):
            return
        _settings = json.loads(worker_config)
        if not isinstance(_settings, dict):
            return

        debug = _settings.get("debug", None)
        detailed_debug = _settings.get("detailed_debug", None)
        if debug is True:  # this needs to be first, so users can see Router init debugg
            import logging

            from litellm._logging import (
                verbose_logger,
                verbose_proxy_logger,
                verbose_router_logger,
            )

            # this must ALWAYS remain logging.INFO, DO NOT MODIFY THIS
            verbose_logger.setLevel(level=logging.INFO)  # sets package logs to info
            verbose_router_logger.setLevel(
                level=logging.INFO
            )  # set router logs to info
            verbose_proxy_logger.setLevel(level=logging.INFO)  # set proxy logs to info
        if detailed_debug is True:
            import logging

            from litellm._logging import (
                verbose_logger,
                verbose_proxy_logger,
                verbose_router_logger,
            )

            verbose_logger.setLevel(level=logging.DEBUG)  # set package log to debug
            verbose_router_logger.setLevel(
                level=logging.DEBUG
            )  # set router logs to debug
            verbose_proxy_logger.setLevel(
                level=logging.DEBUG
            )  # set proxy logs to debug
        elif debug is False and detailed_debug is False:
            # users can control proxy debugging using env variable = 'LITELLM_LOG'
            litellm_log_setting = os.environ.get("LITELLM_LOG", "")
            if litellm_log_setting is not None:
                if litellm_log_setting.upper() == "INFO":
                    import logging

                    from litellm._logging import (
                        verbose_proxy_logger,
                        verbose_router_logger,
                    )

                    # this must ALWAYS remain logging.INFO, DO NOT MODIFY THIS

                    verbose_router_logger.setLevel(
                        level=logging.INFO
                    )  # set router logs to info
                    verbose_proxy_logger.setLevel(
                        level=logging.INFO
                    )  # set proxy logs to info
                elif litellm_log_setting.upper() == "DEBUG":
                    import logging

                    from litellm._logging import (
                        verbose_proxy_logger,
                        verbose_router_logger,
                    )

                    verbose_router_logger.setLevel(
                        level=logging.DEBUG
                    )  # set router logs to info
                    verbose_proxy_logger.setLevel(
                        level=logging.DEBUG
                    )  # set proxy logs to debug
    except Exception as e:
        import logging

        logging.warning(f"Failed to init verbose loggers: {str(e)}")

