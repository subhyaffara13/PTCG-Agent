
def test_may_share_memory_harder_fuzz():
    # Overlap problems with not necessarily common strides take more
    # work.
    #
    # The work bound below can't be reduced much. Harder problems can
    # also exist but not be detected here, as the set of problems
    # comes from RNG.

    check_may_share_memory_easy_fuzz(get_max_work=lambda a, b: max(a.size, b.size) // 2,
                                     same_steps=False,
                                     min_count=2000)

