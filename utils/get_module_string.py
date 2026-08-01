
def get_module_string(gm: torch.fx.GraphModule) -> str:
    def _convert_to_comment(s_: str) -> str:
        s = s_.split("\n")
        if len(s) == 1:
            return "# " + s_
        first = s.pop(0)
        for i in range(len(s)):
            line = s[i]
            if line.strip() != "":
                s[i] = "# " + line
            else:
                s[i] = ""
        s = "\n".join(s)
        s = first + "\n" + s
        return s

    module_string = NNModuleToString.convert(gm)
    return _convert_to_comment(module_string)

