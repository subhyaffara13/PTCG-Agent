
def _warn_on_unsupported_keys(unsupported_keys):
    if unsupported_keys:
        warnings.warn(f"The following metadata cannot be exported to the text notebook: {sorted(unsupported_keys)}")

