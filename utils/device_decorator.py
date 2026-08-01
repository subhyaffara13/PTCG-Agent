
def device_decorator(device, func):
    return context_decorator(lambda: device, func)

