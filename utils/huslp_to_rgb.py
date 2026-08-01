
def huslp_to_rgb(h, s, l):
    return lch_to_rgb(*huslp_to_lch([h, s, l]))

