
def _error_line(error, obj, refimported):
    import traceback
    line = traceback.format_exc().splitlines()[-2].replace('[obj]', '['+repr(obj)+']')
    return "while testing (with refimported=%s):  %s" % (refimported, line.lstrip())

