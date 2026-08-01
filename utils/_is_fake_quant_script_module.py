
def _is_fake_quant_script_module(mod):
    """Return true if given mod is an instance of FakeQuantize script module."""
    if isinstance(mod, torch.jit.RecursiveScriptModule):
        # qualified name looks like '__torch__.torch.ao.quantization.fake_quantize.___torch_mangle_2.FakeQuantize'
        suffix = mod._c.qualified_name.split(".", 1)[1]
        name = re.sub(r"\.___torch_mangle_\d+", "", suffix)
        return (
            name == "torch.ao.quantization.fake_quantize.FakeQuantize"
            or name
            == "torch.ao.quantization.fake_quantize.FusedMovingAvgObsFakeQuantize"
        )
    return False

