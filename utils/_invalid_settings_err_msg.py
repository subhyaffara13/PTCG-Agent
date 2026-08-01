
def _invalid_settings_err_msg(settings, verbose=False):
    valid_settings = (
        ["all"]
        + list(log_registry.log_alias_to_log_qnames.keys())
        + list(log_registry.artifact_names)
    )
    valid_settings = ", ".join(sorted(valid_settings))
    msg = f"""
Invalid log settings: {settings}, must be a comma separated list of fully
qualified module names, registered log names or registered artifact names.
For more info on various settings, try TORCH_LOGS="help"
Valid settings:
{valid_settings}
"""
    return msg

