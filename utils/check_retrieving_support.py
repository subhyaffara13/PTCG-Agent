
def check_retrieving_support(distfn, args):
    loc, scale = 1, 2
    supp = distfn.support(*args)
    supp_loc_scale = distfn.support(*args, loc=loc, scale=scale)
    npt.assert_almost_equal(np.array(supp)*scale + loc,
                            np.array(supp_loc_scale))

