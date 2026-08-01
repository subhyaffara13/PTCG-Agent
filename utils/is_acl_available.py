
def is_acl_available():
    r"""Return whether PyTorch is built with MKL-DNN + ACL support."""
    # pyrefly: ignore [missing-attribute]
    return torch._C._has_mkldnn_acl

