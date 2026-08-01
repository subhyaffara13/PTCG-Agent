
def test_objects(verbose=True):
    for member in objects.keys():
       #pickles(member, exact=True, verbose=verbose)
        pickles(member, exact=False, verbose=verbose)

