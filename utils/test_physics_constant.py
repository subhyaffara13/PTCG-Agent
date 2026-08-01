
def test_physics_constant():
    from sympy.physics.units import definitions

    for name in dir(definitions):
        quantity = getattr(definitions, name)
        if not isinstance(quantity, Quantity):
            continue
        if name.endswith('_constant'):
            assert isinstance(quantity, PhysicalConstant), f"{quantity} must be PhysicalConstant, but is {type(quantity)}"
            assert quantity.is_physical_constant, f"{name} is not marked as physics constant when it should be"

    for const in [gravitational_constant, molar_gas_constant, vacuum_permittivity, speed_of_light, elementary_charge]:
        assert isinstance(const, PhysicalConstant), f"{const} must be PhysicalConstant, but is {type(const)}"
        assert const.is_physical_constant, f"{const} is not marked as physics constant when it should be"

    assert not meter.is_physical_constant
    assert not joule.is_physical_constant

