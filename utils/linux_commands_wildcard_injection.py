
def linux_commands_wildcard_injection(context, config):
    if not ("shell" in config and "subprocess" in config):
        return

    vulnerable_funcs = ["chown", "chmod", "tar", "rsync"]
    if context.call_function_name_qual in config["shell"] or (
        context.call_function_name_qual in config["subprocess"]
        and context.check_call_arg_value("shell", "True")
    ):
        if context.call_args_count >= 1:
            call_argument = context.get_call_arg_at_position(0)
            argument_string = ""
            if isinstance(call_argument, list):
                for li in call_argument:
                    argument_string += f" {li}"
            elif isinstance(call_argument, str):
                argument_string = call_argument

            if argument_string != "":
                for vulnerable_func in vulnerable_funcs:
                    if (
                        vulnerable_func in argument_string
                        and "*" in argument_string
                    ):
                        return bandit.Issue(
                            severity=bandit.HIGH,
                            confidence=bandit.MEDIUM,
                            cwe=issue.Cwe.IMPROPER_WILDCARD_NEUTRALIZATION,
                            text="Possible wildcard injection in call: %s"
                            % context.call_function_name_qual,
                            lineno=context.get_lineno_for_call_arg("shell"),
                        )

