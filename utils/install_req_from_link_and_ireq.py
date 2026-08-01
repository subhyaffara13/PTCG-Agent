
def install_req_from_link_and_ireq(
    link: Link, ireq: InstallRequirement
) -> InstallRequirement:
    return InstallRequirement(
        req=ireq.req,
        comes_from=ireq.comes_from,
        editable=ireq.editable,
        link=link,
        markers=ireq.markers,
        isolated=ireq.isolated,
        hash_options=ireq.hash_options,
        config_settings=ireq.config_settings,
        user_supplied=ireq.user_supplied,
    )

