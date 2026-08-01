
def test_tutorial_stft_sliding_win():
    """Verify example in "Sliding Windows" subsection from the "User Guide".

    In :ref:`tutorial_stft_sliding_win` (file ``signal.rst``) of the
    :ref:`user_guide` the behavior the border behavior of
    ``ShortTimeFFT(np.ones(6), 2, fs=1)`` with a 50 sample signal is discussed.
    This test verifies the presented indexes.
    """
    SFT = ShortTimeFFT(np.ones(6), 2, fs=1)

    # Lower border:
    assert SFT.m_num_mid == 3, f"Slice middle is not 3 but {SFT.m_num_mid=}"
    assert SFT.p_min == -1, f"Lowest slice {SFT.p_min=} is not -1"
    assert SFT.k_min == -5, f"Lowest slice sample {SFT.p_min=} is not -5"
    k_lb, p_lb = SFT.lower_border_end
    assert p_lb == 2, f"First unaffected slice {p_lb=} is not 2"
    assert k_lb == 5, f"First unaffected sample {k_lb=} is not 5"

    n = 50  # upper signal border
    assert (p_max := SFT.p_max(n)) == 27, f"Last slice {p_max=} must be 27"
    assert (k_max := SFT.k_max(n)) == 55, f"Last sample {k_max=} must be 55"
    k_ub, p_ub = SFT.upper_border_begin(n)
    assert p_ub == 24, f"First upper border slice {p_ub=} must be 24"
    assert k_ub == 45, f"First upper border slice {k_ub=} must be 45"

