
def is_special_file(rel_filepath) -> bool:
    _deprecated("is_special_file")
    if is_pytorch_file(rel_filepath):
        if "sparse" in rel_filepath.lower():
            return True
        elif "linalg" in rel_filepath.lower():
            if "batchlinearalgebralibblas" in rel_filepath.lower():
                return False  # don't use "special" mappings for this specific linalg cublas file
            return True
    return False

