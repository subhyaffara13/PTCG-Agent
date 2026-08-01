
def _make_install_req_from_dist(
    dist: BaseDistribution, template: InstallRequirement
) -> InstallRequirement:
    if template.req:
        line = str(template.req)
    elif template.link:
        line = f"{dist.canonical_name} @ {template.link.url}"
    else:
        line = f"{dist.canonical_name}=={dist.version}"
    ireq = install_req_from_line(
        line,
        user_supplied=template.user_supplied,
        comes_from=template.comes_from,
        isolated=template.isolated,
        constraint=template.constraint,
        hash_options=template.hash_options,
        config_settings=template.config_settings,
    )
    ireq.satisfied_by = dist
    return ireq

