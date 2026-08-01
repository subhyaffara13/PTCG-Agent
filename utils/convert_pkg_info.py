
def convert_pkg_info(pkginfo: str, metadata: Message) -> None:
    parsed_message = Parser().parsestr(pkginfo)
    for key, value in parsed_message.items():
        key_lower = key.lower()
        if value == "UNKNOWN":
            continue

        if key_lower == "description":
            description_lines = value.splitlines()
            if description_lines:
                value = "\n".join(
                    (
                        description_lines[0].lstrip(),
                        dedent("\n".join(description_lines[1:])),
                        "\n",
                    )
                )
            else:
                value = "\n"

            metadata.set_payload(value)
        elif key_lower == "home-page":
            metadata.add_header("Project-URL", f"Homepage, {value}")
        elif key_lower == "download-url":
            metadata.add_header("Project-URL", f"Download, {value}")
        else:
            metadata.add_header(key, value)

    metadata.replace_header("Metadata-Version", "2.4")

