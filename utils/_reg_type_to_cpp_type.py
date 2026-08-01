
def _reg_type_to_cpp_type(reg_type: str):
    if reg_type == "string":
        return "std::string"
    return reg_type

