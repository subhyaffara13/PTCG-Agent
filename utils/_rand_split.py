
def _rand_split(arrays, weights, axis, split_per, seed=None):
    # Coerce `arrays` to float64 if integer, to avoid nan-to-integer issues
    arrays = [arr.astype(np.float64) if np.issubdtype(arr.dtype, np.integer)
              else arr for arr in arrays]

    # inverse operation for stats.collapse_weights
    weights = np.array(weights, dtype=np.float64)  # modified inplace; need a copy
    seeded_rand = np.random.RandomState(seed)

    def mytake(a, ix, axis):
        record = np.asanyarray(np.take(a, ix, axis=axis))
        return record.reshape([a.shape[i] if i != axis else 1
                               for i in range(a.ndim)])

    n_obs = arrays[0].shape[axis]
    assert all(a.shape[axis] == n_obs for a in arrays), \
           "data must be aligned on sample axis"
    for i in range(int(split_per) * n_obs):
        split_ix = seeded_rand.randint(n_obs + i)
        prev_w = weights[split_ix]
        q = seeded_rand.rand()
        weights[split_ix] = q * prev_w
        weights = np.append(weights, (1. - q) * prev_w)
        arrays = [np.append(a, mytake(a, split_ix, axis=axis),
                            axis=axis) for a in arrays]
    return arrays, weights

