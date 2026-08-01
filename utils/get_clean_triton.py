
def get_clean_triton(
    input_path: Path,
    output_path: Path = Path("triton_only_repro.py"),
    auto_generate_params: bool = True,
):
    """Run experiments and output results to file

    Args:
        input_path (Path): Path to inductor generated output codede
        output_path (Path): Path to write out the new python file
        auto_generate_params (bool): Whether to automatically generate launch_params if missing
    """
    return process_file(str(input_path), str(output_path), auto_generate_params)

