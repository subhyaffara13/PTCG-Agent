
def test_recursive_vector():
    recursive_vector = m.RecursiveVector()
    recursive_vector.append(m.RecursiveVector())
    recursive_vector[0].append(m.RecursiveVector())
    recursive_vector[0].append(m.RecursiveVector())
    # Can't use len() since test_stl_binders.cpp does not include stl.h,
    # so the necessary conversion is missing
    assert recursive_vector[0].count(m.RecursiveVector()) == 2

