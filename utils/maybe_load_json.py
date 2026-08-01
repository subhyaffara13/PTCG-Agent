
def maybe_load_json(filename):
    if os.path.isfile(filename):
        with open(filename) as fp:
            return json.load(fp)
    log.warning("Attempted to load json file '%s' but it does not exist.", filename)
    return {}

