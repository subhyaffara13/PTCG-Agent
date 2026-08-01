
def test_particle_default():
    # Test default
    p = Particle('P')
    assert p.name == 'P'
    assert p.mass == symbols('P_mass')
    assert p.masscenter.name == 'P_masscenter'
    assert p.potential_energy == 0
    assert p.__str__() == 'P'
    assert p.__repr__() == ("Particle('P', masscenter=P_masscenter, "
                            "mass=P_mass)")
    raises(AttributeError, lambda: p.frame)

