
def convert_typeddict_type(self: TypedDictType) -> Json:
    return {
        ".class": "TypedDictType",
        "items": [[n, convert_type(t)] for (n, t) in self.items.items()],
        "required_keys": sorted(self.required_keys),
        "readonly_keys": sorted(self.readonly_keys),
        "fallback": convert_type(self.fallback),
    }

