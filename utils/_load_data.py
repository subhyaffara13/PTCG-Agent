import os

def _load_data(name):
    """
    Load npz data file under data/
    Returns a copy of the data, rather than keeping the npz file open.
    """
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'data', name)
    with np.load(filename) as f:
        return dict(f.items())

