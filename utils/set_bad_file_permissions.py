
def set_bad_file_permissions(context):
    if "chmod" in context.call_function_name:
        if context.call_args_count == 2:
            mode = context.get_call_arg_at_position(1)

            if (
                mode is not None
                and isinstance(mode, int)
                and _stat_is_dangerous(mode)
            ):
                # world writable is an HIGH, group executable is a MEDIUM
                if mode & stat.S_IWOTH:
                    sev_level = bandit.HIGH
                else:
                    sev_level = bandit.MEDIUM

                filename = context.get_call_arg_at_position(0)
                if filename is None:
                    filename = "NOT PARSED"
                return bandit.Issue(
                    severity=sev_level,
                    confidence=bandit.HIGH,
                    cwe=issue.Cwe.INCORRECT_PERMISSION_ASSIGNMENT,
                    text="Chmod setting a permissive mask %s on file (%s)."
                    % (oct(mode), filename),
                )

