
def check_cudnn_version():
  # check if cuDNN is installed
  if cuda_versions is None:
    raise RuntimeError("cuDNN is not detected.")
  return cuda_versions.cudnn_get_version()

