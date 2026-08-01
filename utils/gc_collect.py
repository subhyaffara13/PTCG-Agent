
def gc_collect():
    """Run the garbage collector twice (needed when running
    reference counting tests with PyPy)"""
    gc.collect()
    gc.collect()

