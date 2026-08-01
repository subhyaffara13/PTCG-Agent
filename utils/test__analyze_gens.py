
def test__analyze_gens():
    assert _analyze_gens((x, y, z)) == (x, y, z)
    assert _analyze_gens([x, y, z]) == (x, y, z)

    assert _analyze_gens(([x, y, z],)) == (x, y, z)
    assert _analyze_gens(((x, y, z),)) == (x, y, z)

