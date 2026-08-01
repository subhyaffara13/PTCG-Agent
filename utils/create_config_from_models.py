
def create_config_from_models(
    model_files: typing.Iterable[pathlib.Path], output_file: pathlib.Path, enable_type_reduction: bool
):
    """
    Create a configuration file with required operators and optionally required types.
    :param model_files: Model files to use to generate the configuration file.
    :param output_file: File to write configuration to.
    :param enable_type_reduction: Include required type information for individual operators in the configuration.
    """

    required_ops, op_type_processors = _extract_ops_and_types_from_ort_models(model_files, enable_type_reduction)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w") as out:
        out.write("# Generated from model/s:\n")
        out.writelines(f"# - {model_file}\n" for model_file in sorted(model_files))

        for domain in sorted(required_ops.keys()):
            for opset in sorted(required_ops[domain].keys()):
                ops = required_ops[domain][opset]
                if ops:
                    out.write(f"{domain};{opset};")
                    if enable_type_reduction:
                        # type string is empty if op hasn't been seen
                        entries = [
                            "{}{}".format(op, op_type_processors.get_config_entry(domain, op) or "")
                            for op in sorted(ops)
                        ]
                    else:
                        entries = sorted(ops)

                    out.write("{}\n".format(",".join(entries)))

    log.info("Created config in %s", output_file)

