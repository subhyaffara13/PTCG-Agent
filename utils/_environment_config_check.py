
def _environment_config_check(environment: _env_bound) -> _env_bound:
    """Perform a sanity check on the environment."""
    assert issubclass(
        environment.undefined, Undefined
    ), "'undefined' must be a subclass of 'jinja2.Undefined'."
    assert (
        environment.block_start_string
        != environment.variable_start_string
        != environment.comment_start_string
    ), "block, variable and comment start strings must be different."
    assert environment.newline_sequence in {
        "\r",
        "\r\n",
        "\n",
    }, "'newline_sequence' must be one of '\\n', '\\r\\n', or '\\r'."
    return environment

