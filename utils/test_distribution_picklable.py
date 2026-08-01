
def test_distribution_picklable():
    pickle.loads(pickle.dumps(Distribution()))

