import time

def timestampToString(value):
    return asctime(time.gmtime(max(0, value + epoch_diff)))

