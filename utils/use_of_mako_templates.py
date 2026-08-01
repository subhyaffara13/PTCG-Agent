
def use_of_mako_templates(context):
    # check type just to be safe
    if isinstance(context.call_function_name_qual, str):
        qualname_list = context.call_function_name_qual.split(".")
        func = qualname_list[-1]
        if "mako" in qualname_list and func == "Template":
            # unlike Jinja2, mako does not have a template wide autoescape
            # feature and thus each variable must be carefully sanitized.
            return bandit.Issue(
                severity=bandit.MEDIUM,
                confidence=bandit.HIGH,
                cwe=issue.Cwe.BASIC_XSS,
                text="Mako templates allow HTML/JS rendering by default and "
                "are inherently open to XSS attacks. Ensure variables "
                "in all templates are properly sanitized via the 'n', "
                "'h' or 'x' flags (depending on context). For example, "
                "to HTML escape the variable 'data' do ${ data |h }.",
            )

