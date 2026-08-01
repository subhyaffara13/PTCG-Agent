
def convert_unpack_type(self: UnpackType) -> Json:
    return {".class": "UnpackType", "type": convert_type(self.type)}

