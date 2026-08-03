import os

def create_minified_hlo_graph(
    minified_fx_graph: fx.GraphModule, inputs: Sequence[torch.Tensor]
) -> None:
    """
    Takes minified FX graph as primary input, and ports it to HLO via StableHLO
    Provides minified HLO graph as output, and archive them to local directory
    """
    hlo_dir = f"{os.getcwd()}/hlo_files"
    os.makedirs(hlo_dir, exist_ok=True)

    from torch_xla.stablehlo import save_torch_model_as_stablehlo

    save_torch_model_as_stablehlo(minified_fx_graph, inputs, hlo_dir)

