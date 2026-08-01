
def _comma_sep_to_list(string):
    return [x_strip for x in string.strip().split(",") if (x_strip := x.strip())]

