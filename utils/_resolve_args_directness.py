
def _resolve_args_directness(
    argnames: Sequence[str],
    indirect: bool | Sequence[str],
    nodeid: str,
) -> dict[str, Literal["indirect", "direct"]]:
    """Resolve if each parametrized argument must be considered an indirect
    parameter to a fixture of the same name, or a direct parameter to the
    parametrized function, based on the ``indirect`` parameter of the
    parametrize() call.

    :param argnames:
        List of argument names passed to ``parametrize()``.
    :param indirect:
        Same as the ``indirect`` parameter of ``parametrize()``.
    :param nodeid:
        Node ID to which the parametrization is applied.
    :returns:
        A dict mapping each arg name to either "indirect" or "direct".
    """
    arg_directness: dict[str, Literal["indirect", "direct"]]
    if isinstance(indirect, bool):
        arg_directness = dict.fromkeys(argnames, "indirect" if indirect else "direct")
    elif isinstance(indirect, Sequence):
        arg_directness = dict.fromkeys(argnames, "direct")
        for arg in indirect:
            if arg not in argnames:
                fail(
                    f"In {nodeid}: indirect fixture '{arg}' doesn't exist",
                    pytrace=False,
                )
            arg_directness[arg] = "indirect"
    else:
        fail(
            f"In {nodeid}: expected Sequence or boolean for indirect, got {type(indirect).__name__}",
            pytrace=False,
        )
    return arg_directness

