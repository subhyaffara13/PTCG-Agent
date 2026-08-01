
def validate_shape_inference_header(
    shape_inference_hdr: str, expected_shape_infr_decls: list[str]
) -> None:
    try:
        with open(shape_inference_hdr) as f:
            shape_infr_decls = f.read()
            shape_infr_decl_lines = set(shape_infr_decls.split("\n"))
    except OSError as e:
        raise AssertionError(
            f"Unable to read from the specified shape_inference_hdr file: {shape_inference_hdr}"
        ) from e

    # TODO(whc) add a check for shape inference functions that have meta kernels implement and should be retired.

    missing_decls = [
        decl for decl in expected_shape_infr_decls if decl not in shape_infr_decl_lines
    ]
    if missing_decls:
        raise Exception(  # noqa: TRY002
            f"""Missing shape inference function.\n
Please add declare this function in {shape_inference_hdr}:\n
and implement it in the corresponding shape_inference.cpp file.\n
{os.linesep.join(missing_decls)}"""
        )

