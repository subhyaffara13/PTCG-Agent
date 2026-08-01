
def convert_tuple_type(self: TupleType) -> Json:
    return {
        ".class": "TupleType",
        "items": [convert_type(t) for t in self.items],
        "partial_fallback": convert_type(self.partial_fallback),
        "implicit": self.implicit,
    }

