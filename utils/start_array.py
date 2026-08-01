
def start_array(self: PlistTarget) -> None:
    a: List[PlistEncodable] = []
    self.add_object(a)
    self.stack.append(a)

