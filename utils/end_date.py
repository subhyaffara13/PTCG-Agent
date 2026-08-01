
def end_date(self: PlistTarget) -> None:
    self.add_object(_date_from_string(self.get_data()))

