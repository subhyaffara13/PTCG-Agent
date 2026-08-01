
def script_add_ones_with_record_function(x, block: str):
    with record_function(block):
        return torch.add(x, torch.ones(1))

