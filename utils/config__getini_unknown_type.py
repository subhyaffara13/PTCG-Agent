
def Config__getini_unknown_type(self, name: str, type: str, value: str | list[str]):
    if type == "pathlist":
        # TODO: This assert is probably not valid in all cases.
        assert self.inipath is not None
        dp = self.inipath.parent
        input_values = shlex.split(value) if isinstance(value, str) else value
        return [legacy_path(str(dp / x)) for x in input_values]
    else:
        raise ValueError(f"unknown configuration type: {type}", value)

