
def prune_hints(self):
    for name in ["XPlaDevice", "YPlaDevice", "XAdvDevice", "YAdvDevice"]:
        v = getattr(self, name, None)
        if v is not None and v.is_hinting():
            delattr(self, name)


def prune_hints(self):
    if self.Format == 2:
        self.Format = 1
    elif self.Format == 3:
        for name in ("XDeviceTable", "YDeviceTable"):
            v = getattr(self, name, None)
            if v is not None and v.is_hinting():
                setattr(self, name, None)
        if self.XDeviceTable is None and self.YDeviceTable is None:
            self.Format = 1

