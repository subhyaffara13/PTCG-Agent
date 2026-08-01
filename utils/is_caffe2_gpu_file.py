
def is_caffe2_gpu_file(rel_filepath):
    _deprecated("is_caffe2_gpu_file")
    if os.path.isabs(rel_filepath):
        raise AssertionError("rel_filepath must be a relative path")
    if rel_filepath.startswith("c10/cuda"):
        return True
    filename = os.path.basename(rel_filepath)
    _, ext = os.path.splitext(filename)

    return ('gpu' in filename or ext in ['.cu', '.cuh']) and ('cudnn' not in filename)

