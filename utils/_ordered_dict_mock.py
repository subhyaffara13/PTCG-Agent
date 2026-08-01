
def _ordered_dict_mock():
    base_ordered_dict_class = """
    class OrderedDict(dict):
        def __reversed__(self): return self[::-1]
        def move_to_end(self, key, last=False): pass
        @classmethod
        def __class_getitem__(cls, item): return cls"""
    return base_ordered_dict_class

