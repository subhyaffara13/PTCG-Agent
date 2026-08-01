
def test_main_namespace_all_dir_coherence():
    """
    Checks if `dir(np)` and `np.__all__` are consistent and return
    the same content, excluding exceptions and private members.
    """
    def _remove_private_members(member_set):
        return {m for m in member_set if not m.startswith('_')}

    def _remove_exceptions(member_set):
        return member_set.difference({
            "bool"  # included only in __dir__
        })

    all_members = _remove_private_members(np.__all__)
    all_members = _remove_exceptions(all_members)

    dir_members = _remove_private_members(np.__dir__())
    dir_members = _remove_exceptions(dir_members)

    assert all_members == dir_members, (
        "Members that break symmetry: "
        f"{all_members.symmetric_difference(dir_members)}"
    )

