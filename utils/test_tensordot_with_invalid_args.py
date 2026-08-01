
def test_tensordot_with_invalid_args():
    rng = np.random.default_rng(23409823)

    arr_a = random_array((3,4,5), density=0.6, random_state=rng, dtype=int)
    arr_b = random_array((3,4,6), density=0.6, random_state=rng, dtype=int)

    axes = ([2], [2]) # sizes of 2nd axes of both shapes do not match
    with pytest.raises(ValueError, match="sizes of the corresponding axes must match"):
        arr_a.tensordot(arr_b, axes=axes)

    arr_a = random_array((5,4,2,3,7), density=0.6, random_state=rng, dtype=int)
    arr_b = random_array((4,6,3,2), density=0.6, random_state=rng, dtype=int)

    axes = ([2,0,1], [1,3]) # lists have different lengths
    with pytest.raises(ValueError, match="axes lists/tuples must be of the"
                       " same length"):
        arr_a.tensordot(arr_b, axes=axes)

