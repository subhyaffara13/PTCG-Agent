
def convert_type_type(self: TypeType) -> Json:
    return {".class": "TypeType", "item": convert_type(self.item)}

