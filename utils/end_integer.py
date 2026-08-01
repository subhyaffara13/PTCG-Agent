
def end_integer(self: PlistTarget) -> None:
    self.add_object(int(self.get_data()))

