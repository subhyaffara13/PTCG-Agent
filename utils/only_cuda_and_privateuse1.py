
def onlyCUDAAndPRIVATEUSE1(fn):
    @wraps(fn)
    def only_fn(self, *args, **kwargs):
        if self.device_type not in ("cuda", torch._C._get_privateuse1_backend_name()):
            reason = f"onlyCUDAAndPRIVATEUSE1: doesn't run on {self.device_type}"
            raise unittest.SkipTest(reason)

        return fn(self, *args, **kwargs)

    return only_fn

