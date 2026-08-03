import os

def remove_extension_h_precompiler_headers() -> None:
    def _remove_if_file_exists(path_file) -> None:
        if os.path.exists(path_file):
            os.remove(path_file)

    head_file_pch = os.path.join(_TORCH_PATH, 'include', 'torch', 'extension.h.gch')
    head_file_signature = os.path.join(_TORCH_PATH, 'include', 'torch', 'extension.h.sign')

    _remove_if_file_exists(head_file_pch)
    _remove_if_file_exists(head_file_signature)

