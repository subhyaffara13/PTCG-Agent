
def _l1_norm(sample: np.ndarray) -> float:
    return distance.pdist(sample, 'cityblock').min()

