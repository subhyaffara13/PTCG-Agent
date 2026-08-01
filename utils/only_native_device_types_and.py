
def onlyNativeDeviceTypesAnd(devices=None):
    def decorator(fn):
        @wraps(fn)
        def only_fn(self, *args, **kwargs):
            if (
                self.device_type not in NATIVE_DEVICES
                and self.device_type not in devices
            ):
                reason = f"onlyNativeDeviceTypesAnd {devices} : doesn't run on {self.device_type}"
                raise unittest.SkipTest(reason)

            return fn(self, *args, **kwargs)

        return only_fn

    return decorator

