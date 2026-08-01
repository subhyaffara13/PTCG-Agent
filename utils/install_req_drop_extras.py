
def install_req_drop_extras(ireq: InstallRequirement) -> InstallRequirement:
    """
    Creates a new InstallationRequirement using the given template but without
    any extras. Sets the original requirement as the new one's parent
    (comes_from).
    """
    return InstallRequirement(
        req=(
            _set_requirement_extras(ireq.req, set()) if ireq.req is not None else None
        ),
        comes_from=ireq,
        editable=ireq.editable,
        link=ireq.link,
        markers=ireq.markers,
        isolated=ireq.isolated,
        hash_options=ireq.hash_options,
        constraint=ireq.constraint,
        extras=[],
        config_settings=ireq.config_settings,
        user_supplied=ireq.user_supplied,
        permit_editable_wheels=ireq.permit_editable_wheels,
    )

