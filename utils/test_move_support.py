
def test_move_support():
    class NCVirtExt(m.NCVirt):
        def get_noncopyable(self, a, b):
            # Constructs and returns a new instance:
            return m.NonCopyable(a * a, b * b)

        def get_movable(self, a, b):
            # Return a referenced copy
            self.movable = m.Movable(a, b)
            return self.movable

    class NCVirtExt2(m.NCVirt):
        def get_noncopyable(self, a, b):
            # Keep a reference: this is going to throw an exception
            self.nc = m.NonCopyable(a, b)
            return self.nc

        def get_movable(self, a, b):
            # Return a new instance without storing it
            return m.Movable(a, b)

    ncv1 = NCVirtExt()
    assert ncv1.print_nc(2, 3) == "36"
    assert ncv1.print_movable(4, 5) == "9"
    ncv2 = NCVirtExt2()
    assert ncv2.print_movable(7, 7) == "14"
    # Don't check the exception message here because it differs under debug/non-debug mode
    with pytest.raises(RuntimeError):
        ncv2.print_nc(9, 9)

    nc_stats = ConstructorStats.get(m.NonCopyable)
    mv_stats = ConstructorStats.get(m.Movable)
    assert nc_stats.alive() == 1
    assert mv_stats.alive() == 1
    del ncv1, ncv2
    assert nc_stats.alive() == 0
    assert mv_stats.alive() == 0
    assert nc_stats.values() == ["4", "9", "9", "9"]
    assert mv_stats.values() == ["4", "5", "7", "7"]
    assert nc_stats.copy_constructions == 0
    assert mv_stats.copy_constructions == 1
    assert nc_stats.move_constructions >= 0
    assert mv_stats.move_constructions >= 0

