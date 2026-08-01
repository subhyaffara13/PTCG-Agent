
def skipCUDAIfRocmHipBlasltVersionLessThan(version=None):
    def dec_fn(fn):
        @wraps(fn)
        def wrap_fn(self, *args, **kwargs):
            if self.device_type == "cuda":
                if not TEST_WITH_ROCM:
                    reason = "ROCm not available"
                    raise unittest.SkipTest(reason)
                hipblaslt_version_tuple = _get_torch_hipblaslt_version()
                if (
                    hipblaslt_version_tuple is None
                    or version is None
                    or hipblaslt_version_tuple < tuple(version)
                ):
                    reason = f"hipBLASLt {hipblaslt_version_tuple} is available but {version} required"
                    raise unittest.SkipTest(reason)

            return fn(self, *args, **kwargs)

        return wrap_fn

    return dec_fn

