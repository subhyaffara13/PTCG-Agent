
def check_for_incompatible_configs() -> None:
    # Some of the configs should be mutually exclusive
    assert not (config.suppress_errors and config.fail_on_recompile_limit_hit), (
        "Dynamo configs suppress_error and fail_on_recompile_limit_hit can not both be active at the same time."
    )

