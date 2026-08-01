
def check_entropy_vect_scale(distfn, arg):
    # check 2-d
    sc = np.asarray([[1, 2], [3, 4]])
    v_ent = distfn.entropy(*arg, scale=sc)
    s_ent = [distfn.entropy(*arg, scale=s) for s in sc.ravel()]
    s_ent = np.asarray(s_ent).reshape(v_ent.shape)
    assert_allclose(v_ent, s_ent, atol=1e-14)

    # check invalid value, check cast
    sc = [1, 2, -3]
    v_ent = distfn.entropy(*arg, scale=sc)
    s_ent = [distfn.entropy(*arg, scale=s) for s in sc]
    s_ent = np.asarray(s_ent).reshape(v_ent.shape)
    assert_allclose(v_ent, s_ent, atol=1e-14)

