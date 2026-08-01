
def make_mvlgamma_opinfo(variant_test_name, domain, skips, sample_kwargs):
    return UnaryUfuncInfo('mvlgamma',
                          ref=reference_mvlgamma if TEST_SCIPY else None,
                          aliases=('special.multigammaln',),
                          variant_test_name=variant_test_name,
                          domain=domain,
                          decorators=(precisionOverride({torch.float16: 5e-2}),),
                          dtypes=all_types_and(torch.half, torch.bfloat16),
                          dtypesIfCUDA=all_types_and(torch.float16, torch.bfloat16),
                          sample_inputs_func=sample_inputs_mvlgamma,
                          supports_forward_ad=True,
                          supports_fwgrad_bwgrad=True,
                          promotes_int_to_float=True,
                          skips=skips,
                          sample_kwargs=sample_kwargs)

