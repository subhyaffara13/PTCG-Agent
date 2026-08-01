
def generate_config_string(*, stable_output: bool = False) -> str:
    import torch._functorch.config
    import torch._inductor.config

    if stable_output:
        return "# config omitted due to stable_output=True"

    experimental_config = torch.fx.experimental._config.codegen_config()  # type: ignore[attr-defined]
    return f"""\
import torch._dynamo.config
import torch._inductor.config
import torch._functorch.config
import torch.fx.experimental._config
{torch._dynamo.config.codegen_config()}
{torch._inductor.config.codegen_config()}
{torch._functorch.config.codegen_config()}
{experimental_config}
"""

