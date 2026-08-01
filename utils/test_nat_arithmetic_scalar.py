
def test_nat_arithmetic_scalar(op_name, value, val_type):
    # see gh-6873
    invalid_ops = {
        "scalar": {"right_div_left"},
        "floating": {
            "right_div_left",
            "left_minus_right",
            "right_minus_left",
            "left_plus_right",
            "right_plus_left",
        },
        "str": set(_ops.keys()),
        "timedelta": {"left_times_right", "right_times_left"},
        "timestamp": {
            "left_times_right",
            "right_times_left",
            "left_div_right",
            "right_div_left",
        },
    }

    op = _ops[op_name]

    if op_name in invalid_ops.get(val_type, set()):
        if (
            val_type == "timedelta"
            and "times" in op_name
            and isinstance(value, Timedelta)
        ):
            typs = "(Timedelta|NaTType)"
            msg = rf"unsupported operand type\(s\) for \*: '{typs}' and '{typs}'"
        elif val_type == "str":
            # un-specific check here because the message comes from str
            #  and varies by method
            msg = "|".join(
                [
                    "can only concatenate str",
                    "unsupported operand type",
                    "can't multiply sequence",
                    "Can't convert 'NaTType'",
                    "must be str, not NaTType",
                ]
            )
        else:
            msg = "unsupported operand type"

        with pytest.raises(TypeError, match=msg):
            op(NaT, value)
    else:
        if val_type == "timedelta" and "div" in op_name:
            expected = np.nan
        else:
            expected = NaT

        assert op(NaT, value) is expected

