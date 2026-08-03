from typing import Any

def _clone_aliasing_output(inputs: Sequence[Any], outputs: Sequence[Any]):
    # For tensors whose grad is None, create zero tensors as gradients
    # This invariant is useful for cudagraph.

    # Elimitate input-output, output-output aliasing
    seen_input_storages = {
        StorageWeakRef(t._typed_storage())
        for t in inputs
        if isinstance(t, torch.Tensor)
    }
    seen_output_storages = set()
    final_outputs = []
    for out in outputs:
        if isinstance(out, torch.Tensor):
            out_storage = StorageWeakRef(out._typed_storage())
            if (
                out_storage in seen_input_storages
                or out_storage in seen_output_storages
            ):
                out = out.clone()
            seen_output_storages.add(StorageWeakRef(out._typed_storage()))
        final_outputs.append(out)
    return final_outputs

