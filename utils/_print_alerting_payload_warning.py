
def _print_alerting_payload_warning(
    payload: dict, slackAlertingInstance: SlackAlertingType
):
    """
    Print the payload to the console when
    slackAlertingInstance.alerting_args.log_to_console is True

    Relevant issue: https://github.com/BerriAI/litellm/issues/7372
    """
    if slackAlertingInstance.alerting_args.log_to_console is True:
        verbose_proxy_logger.warning(payload)

