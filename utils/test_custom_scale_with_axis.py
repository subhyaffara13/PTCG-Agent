
def test_custom_scale_with_axis():
    """
    Test that one can still register and use custom scales with an *axis*
    parameter, but that registering issues a pending-deprecation warning.
    """
    class CustomTransform(IdentityTransform):
        pass

    class CustomScale(mscale.ScaleBase):
        name = "custom"

        # Important: __init__ still has the *axis* parameter
        def __init__(self, axis):
            self._transform = CustomTransform()

        def get_transform(self):
            return self._transform

        def set_default_locators_and_formatters(self, axis):
            axis.set_major_locator(AutoLocator())
            axis.set_major_formatter(ScalarFormatter())
            axis.set_minor_locator(NullLocator())
            axis.set_minor_formatter(NullFormatter())

    try:
        with pytest.warns(
                PendingDeprecationWarning,
                match=r"'axis' parameter .* is pending-deprecated"):
            mscale.register_scale(CustomScale)
        fig, ax = plt.subplots()
        ax.set_xscale('custom')
        assert isinstance(ax.xaxis.get_transform(), CustomTransform)
    finally:
        # cleanup - there's no public unregister_scale()
        del mscale._scale_mapping["custom"]
        del mscale._scale_has_axis_parameter["custom"]

