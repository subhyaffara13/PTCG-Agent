
def convert_literal_type(self: LiteralType) -> Json:
    return {".class": "LiteralType", "value": self.value, "fallback": convert_type(self.fallback)}

