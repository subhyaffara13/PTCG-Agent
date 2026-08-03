from typing import Any

def _prepare_position_ids(model_kwargs: dict[str, Any], new_length: int, is_encoder_decoder: bool) -> dict[str, Any]:
    """Expands or crops the model's position ids for decoding purposes, to the defined length"""

    position_key = "decoder_position_ids" if is_encoder_decoder else "position_ids"
    if model_kwargs.get(position_key) is None:
        return model_kwargs

    positions = model_kwargs[position_key]
    position_length_diff = new_length - positions.shape[-1]

    if position_length_diff < 0:
        model_kwargs[position_key] = positions[:, :position_length_diff]
    elif position_length_diff > 0:
        # Works for 2D and 3D position tensors
        required_dim = [1] * (positions.dim() - 1) + [-1]
        next_position_ids = (
            torch.arange(position_length_diff, dtype=positions.dtype, device=positions.device).view(*required_dim)
            + positions[..., -1:]
            + 1
        )
        next_position_ids = torch.cat([positions, next_position_ids], dim=-1)
        model_kwargs[position_key] = next_position_ids

    return model_kwargs

