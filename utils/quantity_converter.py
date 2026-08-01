
def quantity_converter():
    # Create an instance of the conversion interface and
    # mock so we can check methods called
    qc = munits.ConversionInterface()

    def convert(value, unit, axis):
        if hasattr(value, 'units'):
            return value.to(unit).magnitude
        elif np.iterable(value):
            try:
                return [v.to(unit).magnitude for v in value]
            except AttributeError:
                return [Quantity(v, axis.get_units()).to(unit).magnitude
                        for v in value]
        else:
            return Quantity(value, axis.get_units()).to(unit).magnitude

    def default_units(value, axis):
        if hasattr(value, 'units'):
            return value.units
        elif np.iterable(value):
            for v in value:
                if hasattr(v, 'units'):
                    return v.units
            return None

    qc.convert = MagicMock(side_effect=convert)
    qc.axisinfo = MagicMock(side_effect=lambda u, a:
                            munits.AxisInfo(label=u, default_limits=(0, 100)))
    qc.default_units = MagicMock(side_effect=default_units)
    return qc

