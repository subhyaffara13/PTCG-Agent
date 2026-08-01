
def clear_screen(mode=2):
    return CSI + str(mode) + 'J'

