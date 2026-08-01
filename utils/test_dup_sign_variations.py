
def test_dup_sign_variations():
    assert dup_sign_variations([], ZZ) == 0
    assert dup_sign_variations([1, 0], ZZ) == 0
    assert dup_sign_variations([1, 0, 2], ZZ) == 0
    assert dup_sign_variations([1, 0, 3, 0], ZZ) == 0
    assert dup_sign_variations([1, 0, 4, 0, 5], ZZ) == 0

    assert dup_sign_variations([-1, 0, 2], ZZ) == 1
    assert dup_sign_variations([-1, 0, 3, 0], ZZ) == 1
    assert dup_sign_variations([-1, 0, 4, 0, 5], ZZ) == 1

    assert dup_sign_variations([-1, -4, -5], ZZ) == 0
    assert dup_sign_variations([ 1, -4, -5], ZZ) == 1
    assert dup_sign_variations([ 1, 4, -5], ZZ) == 1
    assert dup_sign_variations([ 1, -4, 5], ZZ) == 2
    assert dup_sign_variations([-1, 4, -5], ZZ) == 2
    assert dup_sign_variations([-1, 4, 5], ZZ) == 1
    assert dup_sign_variations([-1, -4, 5], ZZ) == 1
    assert dup_sign_variations([ 1, 4, 5], ZZ) == 0

    assert dup_sign_variations([-1, 0, -4, 0, -5], ZZ) == 0
    assert dup_sign_variations([ 1, 0, -4, 0, -5], ZZ) == 1
    assert dup_sign_variations([ 1, 0, 4, 0, -5], ZZ) == 1
    assert dup_sign_variations([ 1, 0, -4, 0, 5], ZZ) == 2
    assert dup_sign_variations([-1, 0, 4, 0, -5], ZZ) == 2
    assert dup_sign_variations([-1, 0, 4, 0, 5], ZZ) == 1
    assert dup_sign_variations([-1, 0, -4, 0, 5], ZZ) == 1
    assert dup_sign_variations([ 1, 0, 4, 0, 5], ZZ) == 0

