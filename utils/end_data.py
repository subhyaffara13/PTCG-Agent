
def end_data(self: PlistTarget) -> None:
    if self._use_builtin_types:
        self.add_object(b64decode(self.get_data()))
    else:
        self.add_object(Data.fromBase64(self.get_data()))

