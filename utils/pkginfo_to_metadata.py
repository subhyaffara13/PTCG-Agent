import os

def pkginfo_to_metadata(egg_info_path: str, pkginfo_path: str) -> Message:
    """
    Convert .egg-info directory with PKG-INFO to the Metadata 2.1 format
    """
    with open(pkginfo_path, encoding="utf-8") as headers:
        pkg_info = Parser().parse(headers)

    pkg_info.replace_header("Metadata-Version", "2.1")
    # Those will be regenerated from `requires.txt`.
    del pkg_info["Provides-Extra"]
    del pkg_info["Requires-Dist"]
    requires_path = os.path.join(egg_info_path, "requires.txt")
    if os.path.exists(requires_path):
        with open(requires_path, encoding="utf-8") as requires_file:
            requires = requires_file.read()

        parsed_requirements = sorted(split_sections(requires), key=lambda x: x[0] or "")
        for extra, reqs in parsed_requirements:
            for key, value in generate_requirements({extra: reqs}):
                if (key, value) not in pkg_info.items():
                    pkg_info[key] = value

    description = pkg_info["Description"]
    if description:
        description_lines = pkg_info["Description"].splitlines()
        dedented_description = "\n".join(
            # if the first line of long_description is blank,
            # the first line here will be indented.
            (
                description_lines[0].lstrip(),
                textwrap.dedent("\n".join(description_lines[1:])),
                "\n",
            )
        )
        pkg_info.set_payload(dedented_description)
        del pkg_info["Description"]

    return pkg_info

