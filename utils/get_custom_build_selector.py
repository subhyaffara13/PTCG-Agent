
def get_custom_build_selector(
    provided_op_registration_allowlist: list[str] | None,
    op_selection_yaml_path: str | None,
) -> SelectiveBuilder:
    if (
        provided_op_registration_allowlist is not None
        and op_selection_yaml_path is not None
    ):
        raise AssertionError(
            "Both provided_op_registration_allowlist and op_selection_yaml_path "
            "can NOT be provided at the same time."
        )

    op_registration_allowlist: set[str] | None = None
    if provided_op_registration_allowlist is not None:
        op_registration_allowlist = set(provided_op_registration_allowlist)

    if op_registration_allowlist is not None:
        selector = SelectiveBuilder.from_legacy_op_registration_allow_list(
            op_registration_allowlist,
            True,
            False,
        )
    elif op_selection_yaml_path is not None:
        selector = SelectiveBuilder.from_yaml_path(op_selection_yaml_path)
    else:
        selector = SelectiveBuilder.get_nop_selector()

    return selector

