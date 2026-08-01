
def _is_torchscript_zip(zip_file):
    return "constants.pkl" in zip_file.get_all_records()

