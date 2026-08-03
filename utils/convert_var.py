from typing import Any

def convert_var(self: Var) -> Json:
    data: dict[str, Any] = {
        ".class": "Var",
        "name": self._name,
        "fullname": self._fullname,
        "type": None if self.type is None else convert_type(self.type),
        "setter_type": None if self.setter_type is None else convert_type(self.setter_type),
        "flags": get_flags(self, VAR_FLAGS),
    }
    if self.final_value is not None:
        data["final_value"] = self.final_value
    return data

