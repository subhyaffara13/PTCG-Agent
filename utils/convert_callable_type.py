
def convert_callable_type(self: CallableType) -> Json:
    return {
        ".class": "CallableType",
        "arg_types": [convert_type(t) for t in self.arg_types],
        "arg_kinds": [int(x.value) for x in self.arg_kinds],
        "arg_names": self.arg_names,
        "ret_type": convert_type(self.ret_type),
        "fallback": convert_type(self.fallback),
        "name": self.name,
        # We don't serialize the definition (only used for error messages).
        "variables": [convert_type(v) for v in self.variables],
        "is_ellipsis_args": self.is_ellipsis_args,
        "implicit": self.implicit,
        "is_bound": self.is_bound,
        "type_guard": convert_type(self.type_guard) if self.type_guard is not None else None,
        "type_is": convert_type(self.type_is) if self.type_is is not None else None,
        "from_concatenate": self.from_concatenate,
        "imprecise_arg_kinds": self.imprecise_arg_kinds,
        "unpack_kwargs": self.unpack_kwargs,
    }

