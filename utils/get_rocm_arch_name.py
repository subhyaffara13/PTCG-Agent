
def getRocmArchName(device_index: int = 0):
    return torch.cuda.get_device_properties(device_index).gcnArchName

