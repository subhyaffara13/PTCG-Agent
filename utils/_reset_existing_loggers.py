
def _resetExistingLoggers(parent="root"):
    """Reset the logger named 'parent' and all its children to their initial
    state, if they already exist in the current configuration.
    """
    root = logging.root
    # get sorted list of all existing loggers
    existing = sorted(root.manager.loggerDict.keys())
    if parent == "root":
        # all the existing loggers are children of 'root'
        loggers_to_reset = [parent] + existing
    elif parent not in existing:
        # nothing to do
        return
    elif parent in existing:
        loggers_to_reset = [parent]
        # collect children, starting with the entry after parent name
        i = existing.index(parent) + 1
        prefixed = parent + "."
        pflen = len(prefixed)
        num_existing = len(existing)
        while i < num_existing:
            if existing[i][:pflen] == prefixed:
                loggers_to_reset.append(existing[i])
            i += 1
    for name in loggers_to_reset:
        if name == "root":
            root.setLevel(logging.WARNING)
            for h in root.handlers[:]:
                root.removeHandler(h)
            for f in root.filters[:]:
                root.removeFilters(f)
            root.disabled = False
        else:
            logger = root.manager.loggerDict[name]
            logger.level = logging.NOTSET
            logger.handlers = []
            logger.filters = []
            logger.propagate = True
            logger.disabled = False

