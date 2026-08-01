
def _make_sequence_methods(field_name: str):
    def len_method(self) -> int:
        return len(getattr(self, field_name))

    def iter_method(self):
        return iter(getattr(self, field_name))

    def getitem_method(self, idx):
        return getattr(self, field_name)[idx]

    return len_method, iter_method, getitem_method

