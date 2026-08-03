from typing import Callable

def onlyNativeDeviceTypes(fn: Callable[_P, _T]) -> Callable[_P, _T]:
    @wraps(fn)
    def only_fn(self, *args: _P.args, **kwargs: _P.kwargs) -> _T:
        if self.device_type not in NATIVE_DEVICES:
            reason = f"onlyNativeDeviceTypes: doesn't run on {self.device_type}"
            raise unittest.SkipTest(reason)

        return fn(self, *args, **kwargs)

    return only_fn

