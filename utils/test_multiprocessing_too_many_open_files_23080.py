
def test_multiprocessing_too_many_open_files_23080():
    # https://github.com/scipy/scipy/issues/23080
    x0 = np.array([0.9, 0.9])
    # check that ScalarHessWrapper doesn't keep pool object alive
    with assert_deallocated(multiprocessing.Pool, 2) as pool_obj:
        with pool_obj as p:
            _minimize_bfgs(rosen, x0, workers=p.map)
        del p
        del pool_obj

