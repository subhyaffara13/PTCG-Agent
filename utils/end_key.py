
def end_key(self: PlistTarget) -> None:
    if self.current_key or not isinstance(self.stack[-1], collections.abc.Mapping):
        raise ValueError("unexpected key")
    self.current_key = self.get_data()

