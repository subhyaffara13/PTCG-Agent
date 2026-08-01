
def make_install_req_from_editable(
    link: Link, template: InstallRequirement
) -> InstallRequirement:
    assert template.editable, "template not editable"
    if template.name:
        req_string = f"{template.name} @ {link.url}"
    else:
        req_string = link.url
    ireq = install_req_from_editable(
        req_string,
        user_supplied=template.user_supplied,
        comes_from=template.comes_from,
        isolated=template.isolated,
        constraint=template.constraint,
        permit_editable_wheels=template.permit_editable_wheels,
        hash_options=template.hash_options,
        config_settings=template.config_settings,
    )
    ireq.extras = template.extras
    return ireq

