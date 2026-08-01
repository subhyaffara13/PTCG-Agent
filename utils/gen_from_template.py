
def gen_from_template(
    dir: str,
    template_name: str,
    output_name: str,
    replacements: list[tuple[str, Any, int]],
) -> None:
    template_path = os.path.join(dir, template_name)
    output_path = os.path.join(dir, output_name)

    with open(template_path, encoding="utf-8") as f:
        content = f.read()
    for placeholder, lines, indentation in replacements:
        with open(output_path, "w", encoding="utf-8") as f:
            content = content.replace(
                placeholder, materialize_lines(lines, indentation)
            )
            f.write(content)

