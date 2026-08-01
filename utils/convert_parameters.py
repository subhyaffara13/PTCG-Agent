
def convert_parameters(self: Parameters) -> Json:
    return {
        ".class": "Parameters",
        "arg_types": [convert_type(t) for t in self.arg_types],
        "arg_kinds": [int(x.value) for x in self.arg_kinds],
        "arg_names": self.arg_names,
        "variables": [convert_type(tv) for tv in self.variables],
        "imprecise_arg_kinds": self.imprecise_arg_kinds,
    }

