import os

def test_legacy_pickle(version):
    # Pickling format was changes in 1.22.x and in 2.0.x
    import gzip
    import pickle

    base_path = os.path.split(os.path.abspath(__file__))[0]
    pkl_file = os.path.join(
        base_path, "data", f"generator_pcg64_np{version}.pkl.gz"
    )
    with gzip.open(pkl_file) as gz:
        rg = pickle.load(gz)
    state = rg.bit_generator.state['state']

    assert isinstance(rg, Generator)
    assert isinstance(rg.bit_generator, np.random.PCG64)
    assert state['state'] == 35399562948360463058890781895381311971
    assert state['inc'] == 87136372517582989555478159403783844777

