
def validate_fontsize_None(s):
    if s is None or s == 'None':
        return None
    else:
        return validate_fontsize(s)

