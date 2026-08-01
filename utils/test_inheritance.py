
def test_inheritance(msg):
    roger = m.Rabbit("Rabbit")
    assert roger.name() + " is a " + roger.species() == "Rabbit is a parrot"
    assert m.pet_name_species(roger) == "Rabbit is a parrot"

    polly = m.Pet("Polly", "parrot")
    assert polly.name() + " is a " + polly.species() == "Polly is a parrot"
    assert m.pet_name_species(polly) == "Polly is a parrot"

    molly = m.Dog("Molly")
    assert molly.name() + " is a " + molly.species() == "Molly is a dog"
    assert m.pet_name_species(molly) == "Molly is a dog"

    fred = m.Hamster("Fred")
    assert fred.name() + " is a " + fred.species() == "Fred is a rodent"

    assert m.dog_bark(molly) == "Woof!"

    with pytest.raises(TypeError) as excinfo:
        m.dog_bark(polly)
    assert (
        msg(excinfo.value)
        == """
        dog_bark(): incompatible function arguments. The following argument types are supported:
            1. (arg0: m.class_.Dog) -> str

        Invoked with: <m.class_.Pet object at 0>
    """
    )

    with pytest.raises(TypeError) as excinfo:
        m.Chimera("lion", "goat")
    assert "No constructor defined!" in str(excinfo.value)


def test_inheritance():
    @dispatch(A)
    def f(x): # noqa:F811
        return 'a'

    @dispatch(B) # noqa:F811
    def f(x): # noqa:F811
        return 'b'

    assert f(A()) == 'a'
    assert f(B()) == 'b'
    assert f(C()) == 'a'


def test_inheritance(xp):
    class Empty(interface.LinearOperator):
        pass

    with warns(RuntimeWarning, match="should implement at least"):
        assert_raises(TypeError, Empty)

    class Identity(interface.LinearOperator):
        def __init__(self, n):
            super().__init__(dtype=None, shape=(n, n), xp=xp)

        def _matvec(self, x):
            return x

    id3 = Identity(3)
    xp_assert_equal(id3.matvec(xp.asarray([1, 2, 3])), xp.asarray([1, 2, 3]))
    assert_raises(NotImplementedError, id3.rmatvec, xp.asarray([4, 5, 6]))

    class MatmatOnly(interface.LinearOperator):
        def __init__(self, A):
            super().__init__(A.dtype, A.shape, xp=xp)
            self.A = A

        def _matmat(self, x):
            return self.A @ x

    mm = MatmatOnly(xp.asarray(np.random.randn(5, 3)))
    assert mm.matvec(xp.asarray(np.random.randn(3))).shape == (5,)

