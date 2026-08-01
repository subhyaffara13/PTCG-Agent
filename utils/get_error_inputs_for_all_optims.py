
def get_error_inputs_for_all_optims(device, dtype):
    if _get_device_type(device) == "cpu":
        # Creating 2D parameters for compatibility with Muon.
        sample_param = Parameter(torch.randn(1, 1, device=device, dtype=dtype))
        sample_param2 = Parameter(torch.randn(1, 1, device=device, dtype=dtype))
        return [
            ErrorOptimizerInput(
                OptimizerInput(
                    params=sample_param,
                    kwargs={},
                    desc="invalid param type",
                ),
                error_type=TypeError,
                error_regex="params argument given to the optimizer should be an iterable of Tensors or dicts",
            ),
            ErrorOptimizerInput(
                OptimizerInput(
                    params=[sample_param, sample_param],
                    kwargs={},
                    desc="a param group cannot have duplicate parameters",
                ),
                error_type=UserWarning,
                error_regex=".*a parameter group with duplicate parameters.*",
            ),
            ErrorOptimizerInput(
                OptimizerInput(
                    params=[{"params": sample_param}, {"params": sample_param}],
                    kwargs={},
                    desc="duplicate parameters should not occur across param groups either",
                ),
                error_type=ValueError,
                error_regex="some parameters appear in more than one parameter group",
            ),
            ErrorOptimizerInput(
                OptimizerInput(
                    params=None,
                    kwargs=dict(lr=torch.tensor([0.001, 0.001])),
                    desc="Tensor lr must be 1-element",
                ),
                error_type=ValueError,
                error_regex="Tensor lr must be 1-element",
            ),
            ErrorOptimizerInput(
                OptimizerInput(
                    params=[("weight", sample_param), sample_param2],
                    kwargs={},
                    desc="all optimizer params should be with/without names",
                ),
                error_type=ValueError,
                error_regex="all optimizer params should be with/without names. Some param names are missing",
            ),
            ErrorOptimizerInput(
                OptimizerInput(
                    params=[
                        {"params": [sample_param], "lr": 1e-2},
                        {"params": [("weight", sample_param2)]},
                    ],
                    kwargs={},
                    desc="all optimizer param groups should be with/without names.",
                ),
                error_type=ValueError,
                error_regex="all optimizer param groups should be with/without names. "
                "cannot add param group with names to the optimizer",
            ),
        ]
    else:
        return []

