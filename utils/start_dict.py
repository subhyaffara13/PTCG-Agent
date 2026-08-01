
def start_dict(self: PlistTarget) -> None:
    d = self._dict_type()
    self.add_object(d)
    self.stack.append(d)

