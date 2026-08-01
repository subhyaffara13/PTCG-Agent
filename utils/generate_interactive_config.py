
def generate_interactive_config(linter: PyLinter) -> None:
    print("Starting interactive pylint configuration generation")

    format_type = utils.get_and_validate_format()
    minimal = format_type == "toml" and utils.get_minimal_setting()
    to_file, output_file_name = utils.get_and_validate_output_file()

    if format_type == "toml":
        config_string = linter._generate_config_file(minimal=minimal)
    else:
        output_stream = StringIO()
        linter._generate_config(stream=output_stream, skipsections=("Commands",))
        config_string = output_stream.getvalue()

    if to_file:
        with open(output_file_name, "w", encoding="utf-8") as f:
            print(config_string, file=f)
        print(f"Wrote configuration file to {output_file_name.resolve()}")
    else:
        print(config_string)

