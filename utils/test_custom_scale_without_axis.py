
def test_custom_scale_without_axis():
    """
    Test that one can register and use custom scales that don't take an *axis* param.
    """
    class CustomTransform(IdentityTransform):
        pass

    class CustomScale(mscale.ScaleBase):
        name = "custom"

        # Important: __init__ has no *axis* parameter
        def __init__(self):
            self._transform = CustomTransform()

        def get_transform(self):
            return self._transform

        def set_default_locators_and_formatters(self, axis):
            axis.set_major_locator(AutoLocator())
            axis.set_major_formatter(ScalarFormatter())
            axis.set_minor_locator(NullLocator())
            axis.set_minor_formatter(NullFormatter())

    try:
        mscale.register_scale(CustomScale)
        fig, ax = plt.subplots()
        ax.set_xscale('custom')
        assert isinstance(ax.xaxis.get_transform(), CustomTransform)
    finally:
        # cleanup - there's no public unregister_scale()
        del mscale._scale_mapping["custom"]
        del mscale._scale_has_axis_parameter["custom"]

