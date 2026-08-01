
def test_hyp0f1_gh5764():
    # Do a small and somewhat systematic test that runs quickly
    dataset = []
    axis = [-99.5, -9.5, -0.5, 0.5, 9.5, 99.5]
    for v in axis:
        for x in axis:
            for y in axis:
                z = x + 1j*y
                # mpmath computes the answer correctly at dps ~ 17 but
                # fails for 20 < dps < 120 (uses a different method);
                # set the dps high enough that this isn't an issue
                with mpmath.workdps(120):
                    res = complex(mpmath.hyp0f1(v, z))
                dataset.append((v, z, res))
    dataset = np.array(dataset)

    FuncData(lambda v, z: sc.hyp0f1(v.real, z), dataset, (0, 1), 2,
             rtol=1e-13).check()

