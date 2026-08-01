
def _copytree(input_path, output_path):
    if _samepath(input_path, output_path):
        logger.debug("input and output paths are the same file; skipped copy")
        return
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    shutil.copytree(input_path, output_path)

