
def end_dict(self: PlistTarget) -> None:
    if self.current_key:
        raise ValueError("missing value for key '%s'" % self.current_key)
    self.stack.pop()

