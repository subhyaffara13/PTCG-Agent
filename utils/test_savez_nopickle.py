
def test_savez_nopickle():
    obj_array = np.array([1, 'hello'], dtype=object)
    with temppath(suffix='.npz') as tmp:
        np.savez(tmp, obj_array)

    with temppath(suffix='.npz') as tmp:
        with pytest.raises(ValueError, match="Object arrays cannot be saved when.*"):
            np.savez(tmp, obj_array, allow_pickle=False)

    with temppath(suffix='.npz') as tmp:
        np.savez_compressed(tmp, obj_array)

    with temppath(suffix='.npz') as tmp:
        with pytest.raises(ValueError, match="Object arrays cannot be saved when.*"):
            np.savez_compressed(tmp, obj_array, allow_pickle=False)

