import logging
import pathlib

def analyze_model(model_path: pathlib.Path, skip_optimize: bool = False, logger: logging.Logger | None = None):
    """
    Analyze the provided model to determine if it's likely to work well with the NNAPI or CoreML Execution Providers
    :param model_path: Model to analyze.
    :param skip_optimize: Skip optimizing to BASIC level before checking. When exporting to ORT format we will do this
                          optimization..
    :param logger: Logger for output
    :return: True if either the NNAPI or CoreML Execution Providers may work well with this model.
    """
    if not logger:
        logger = logging.getLogger("usability_checker")
        logger.setLevel(logging.INFO)

    logger.info(f"Checking {model_path} for usability with ORT Mobile.")

    with tempfile.TemporaryDirectory() as tmp:
        if not skip_optimize:
            tmp_path = pathlib.Path(tmp) / model_path.name
            optimize_model(model_path, tmp_path, use_external_initializers=True)
            model_path = tmp_path

        try_eps = checker(model_path.resolve(strict=True), logger)

    return try_eps

