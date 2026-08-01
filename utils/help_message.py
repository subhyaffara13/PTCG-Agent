
def help_message(verbose=False):
    def pad_to(s, length=30):
        if len(s) > length:
            raise AssertionError(f"string length {len(s)} exceeds max {length}")
        return s + " " * (length - len(s))

    if verbose:
        printed_artifacts = log_registry.artifact_names
    else:
        printed_artifacts = log_registry.visible_artifacts
    if verbose:
        heading = "All registered names"
    else:
        heading = "Visible registered names (use TORCH_LOGS='+help' for full list)"
    lines = (
        ["all"]
        + sorted(log_registry.log_alias_to_log_qnames.keys())
        + sorted(
            [
                f"{pad_to(name)}\t{log_registry.artifact_descriptions[name]}"
                for name in printed_artifacts
            ]
        )
    )
    setting_info = "  " + "\n  ".join(lines)
    examples = """
Examples:
  TORCH_LOGS="+dynamo,aot" will set the log level of TorchDynamo to
  logging.DEBUG and AOT to logging.INFO

  TORCH_LOGS="-dynamo,+inductor" will set the log level of TorchDynamo to
  logging.ERROR and TorchInductor to logging.DEBUG

  TORCH_LOGS="aot_graphs" will enable the aot_graphs artifact

  TORCH_LOGS="+dynamo,schedule" will enable set the log level of TorchDynamo
  to logging.DEBUG and enable the schedule artifact

  TORCH_LOGS="+some.random.module,schedule" will set the log level of
  some.random.module to logging.DEBUG and enable the schedule artifact

  TORCH_LOGS="+torch._functorch._aot_autograd" will set the log level of
  torch._functorch._aot_autograd and all its submodules to logging.DEBUG
  (directory-based logging)

  TORCH_LOGS_FORMAT="%(levelname)s: %(message)s" or any provided format
  string will set the output format
  Valid keys are "levelname", "message", "pathname", "levelno", "lineno",
  "filename" and "name".

  TORCH_LOGS_OUT=/tmp/output.txt will output the logs to /tmp/output.txt as
  well. This is useful when the output is long.
"""
    msg = f"""
TORCH_LOGS Info
{examples}

{heading}
{setting_info}
"""
    return msg

