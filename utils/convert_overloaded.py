
def convert_overloaded(self: Overloaded) -> Json:
    return {".class": "Overloaded", "items": [convert_type(t) for t in self.items]}

