
def _copy_extra_directory(source_dir: Path, target_dir: Path, model_list: list[str]):
    """Copy extra directory that does not have onnx model

    Args:
        source_dir (Path): source directory
        target_dir (Path): target directory
        model_list (List[str]): list of directory names with onnx model.

    Raises:
        RuntimeError: source path does not exist
    """
    extra_dirs = ["scheduler", "tokenizer", "tokenizer_2", "tokenizer_3", "feature_extractor"]

    for name in extra_dirs:
        source_path = source_dir / name
        if not os.path.exists(source_path):
            continue

        target_path = target_dir / name
        if target_path.exists():
            shutil.rmtree(target_path)
        shutil.copytree(source_path, target_path)
        logger.info("%s => %s", source_path, target_path)

    extra_files = ["model_index.json"]
    for name in extra_files:
        source_path = source_dir / name
        if not os.path.exists(source_path):
            raise RuntimeError(f"source path does not exist: {source_path}")

        target_path = target_dir / name
        shutil.copyfile(source_path, target_path)
        logger.info("%s => %s", source_path, target_path)

    # Some directory are optional
    for onnx_model_dir in model_list:
        source_path = source_dir / onnx_model_dir / "config.json"
        target_path = target_dir / onnx_model_dir / "config.json"
        if source_path.exists():
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, target_path)
            logger.info("%s => %s", source_path, target_path)

