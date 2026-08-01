
def convert_union_type(self: UnionType) -> Json:
    return {
        ".class": "UnionType",
        "items": [convert_type(t) for t in self.items],
        "uses_pep604_syntax": self.uses_pep604_syntax,
    }

