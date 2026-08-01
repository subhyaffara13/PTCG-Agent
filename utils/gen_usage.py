
def gen_usage(script_name):
    script = os.path.basename(script_name)
    return USAGE % locals()

