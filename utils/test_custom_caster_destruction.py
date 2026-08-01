
def test_custom_caster_destruction():
    """Tests that returning a pointer to a type that gets converted with a custom type caster gets
    destroyed when the function has py::return_value_policy::take_ownership policy applied.
    """

    cstats = m.destruction_tester_cstats()
    # This one *doesn't* have take_ownership: the pointer should be used but not destroyed:
    z = m.custom_caster_no_destroy()
    assert cstats.alive() == 1
    assert cstats.default_constructions == 1
    assert z

    # take_ownership applied: this constructs a new object, casts it, then destroys it:
    z = m.custom_caster_destroy()
    assert z
    assert cstats.default_constructions == 2

    # Same, but with a const pointer return (which should *not* inhibit destruction):
    z = m.custom_caster_destroy_const()
    assert z
    assert cstats.default_constructions == 3

    # Make sure we still only have the original object (from ..._no_destroy()) alive:
    assert cstats.alive() == 1

