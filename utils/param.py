
def param(
    *values: object,
    marks: MarkDecorator | Collection[MarkDecorator | Mark] = (),
    id: str | _HiddenParam | None = None,
) -> ParameterSet:
    """Specify a parameter in `pytest.mark.parametrize`_ calls or
    :ref:`parametrized fixtures <fixture-parametrize-marks>`.

    .. code-block:: python

        @pytest.mark.parametrize(
            "test_input,expected",
            [
                ("3+5", 8),
                pytest.param("6*9", 42, marks=pytest.mark.xfail),
            ],
        )
        def test_eval(test_input, expected):
            assert eval(test_input) == expected

    :param values: Variable args of the values of the parameter set, in order.

    :param marks:
        A single mark or a list of marks to be applied to this parameter set.

        :ref:`pytest.mark.usefixtures <pytest.mark.usefixtures ref>` cannot be added via this parameter.

    :type id: str | Literal[pytest.HIDDEN_PARAM] | None
    :param id:
        The id to attribute to this parameter set.

        .. versionadded:: 8.4
            :ref:`hidden-param` means to hide the parameter set
            from the test name. Can only be used at most 1 time, as
            test names need to be unique.
    """
    return ParameterSet.param(*values, marks=marks, id=id)

