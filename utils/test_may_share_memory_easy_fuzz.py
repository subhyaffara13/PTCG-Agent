
def test_may_share_memory_easy_fuzz():
    # Check that overlap problems with common strides are always
    # solved with little work.

    check_may_share_memory_easy_fuzz(get_max_work=lambda a, b: 1,
                                     same_steps=True,
                                     min_count=2000)

