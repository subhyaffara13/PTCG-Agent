
def test_suppress_warnings_forwarding():
    # NOTE(seberg): We test for the DeprecationWarning mainly because on
    # free-threaded Python an "ignore" warning filters seem to collide with
    # parts of what `suppress_warnings` does (if used more than once?).
    with pytest.warns(
            DeprecationWarning,
            match="suppression and assertion utilities are deprecated"):
        def warn_other_module():
            # Apply along axis is implemented in python; stacklevel=2 means
            # we end up inside its module, not ours.
            def warn(arr):
                warnings.warn("Some warning", stacklevel=2)
                return arr
            np.apply_along_axis(warn, 0, [0])

        with suppress_warnings() as sup:
            sup.record()
            with suppress_warnings("always"):
                for i in range(2):
                    warnings.warn("Some warning")

            # includes a DeprecationWarning for suppress_warnings
            assert_equal(len(sup.log), 3)

        with suppress_warnings() as sup:
            sup.record()
            with suppress_warnings("location"):
                for i in range(2):
                    warnings.warn("Some warning")
                    warnings.warn("Some warning")

            # includes a DeprecationWarning for suppress_warnings
            assert_equal(len(sup.log), 3)

        with suppress_warnings() as sup:
            sup.record()
            with suppress_warnings("module"):
                for i in range(2):
                    warnings.warn("Some warning")
                    warnings.warn("Some warning")
                    warn_other_module()

            # includes a DeprecationWarning for suppress_warnings
            assert_equal(len(sup.log), 3)

        with suppress_warnings() as sup:
            sup.record()
            with suppress_warnings("once"):
                for i in range(2):
                    warnings.warn("Some warning")
                    warnings.warn("Some other warning")
                    warn_other_module()

            # includes a DeprecationWarning for suppress_warnings
            assert_equal(len(sup.log), 3)

