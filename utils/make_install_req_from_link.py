
def make_install_req_from_link(
    link: Link,
    template: InstallRequirement,
    version: Version | None = None,
) -> InstallRequirement:
    assert not template.editable, "template is editable"
    if version is not None and template.req and template.hash_options:
        # When hashes are provided via constraints for an unpinned requirement,
        # the resulting install requirement must appear pinned so that the
        # hash-checking logic does not reject it as HashUnpinned.
        line = f"{template.req.name}=={version}"
    elif template.req:
        line = str(template.req)
    else:
        line = link.url
    ireq = install_req_from_line(
        line,
        user_supplied=template.user_supplied,
        comes_from=template.comes_from,
        isolated=template.isolated,
        constraint=template.constraint,
        hash_options=template.hash_options,
        config_settings=template.config_settings,
    )
    ireq.original_link = template.original_link
    ireq.link = link
    ireq.extras = template.extras
    return ireq

