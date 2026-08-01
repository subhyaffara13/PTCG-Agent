
def get_block_sequence_ids_for_mask(mm_token_type_ids: torch.Tensor, device: torch.device) -> torch.Tensor:
    mm_token_type_ids = mm_token_type_ids.to(device)

    is_vision = (mm_token_type_ids == 1) | (mm_token_type_ids == 2)
    is_prev_vision = torch.roll(is_vision, shifts=1, dims=-1)
    is_prev_vision[..., 0] = False
    new_vision_starts = is_vision & ~is_prev_vision
    vision_group_ids = torch.cumsum(new_vision_starts.int(), dim=1) - 1
    block_sequence_ids = torch.where(is_vision, vision_group_ids, -1)
    return block_sequence_ids


def get_block_sequence_ids_for_mask(token_type_ids: torch.Tensor, device: torch.device | None = None) -> torch.Tensor:
    # First find where a new image block starts: 1 if image and previous not image
    # The images cannot attend to future images, but can attend to all prev images and to itself bidirectionally
    is_image = (token_type_ids == 1).to(device=device)
    is_previous_image = nn.functional.pad(is_image, (1, 0), value=0)[:, :-1]
    new_image_start = is_image & ~is_previous_image
    group_ids = torch.cumsum(new_image_start.int(), dim=1) - 1
    block_sequence_ids = torch.where(is_image, group_ids, -1)
    return block_sequence_ids


def get_block_sequence_ids_for_mask(token_type_ids: torch.Tensor, device: torch.device | None = None) -> torch.Tensor:
    # First find where a new image block starts: 1 if image and previous not image
    # The images cannot attend to future images, but can attend to all prev images and to itself bidirectionally
    is_image = (token_type_ids == 1).to(device=device)
    is_previous_image = nn.functional.pad(is_image, (1, 0), value=0)[:, :-1]
    new_image_start = is_image & ~is_previous_image
    group_ids = torch.cumsum(new_image_start.int(), dim=1) - 1
    block_sequence_ids = torch.where(is_image, group_ids, -1)
    return block_sequence_ids


def get_block_sequence_ids_for_mask(mm_token_type_ids: torch.Tensor, device: torch.device) -> torch.Tensor:
    mm_token_type_ids = mm_token_type_ids.to(device)

    is_vision = (mm_token_type_ids == 1) | (mm_token_type_ids == 2)
    is_prev_vision = torch.roll(is_vision, shifts=1, dims=-1)
    is_prev_vision[..., 0] = False
    new_vision_starts = is_vision & ~is_prev_vision
    vision_group_ids = torch.cumsum(new_vision_starts.int(), dim=1) - 1
    block_sequence_ids = torch.where(is_vision, vision_group_ids, -1)
    return block_sequence_ids


def get_block_sequence_ids_for_mask(mm_token_type_ids: torch.Tensor, device: torch.device) -> torch.Tensor:
    mm_token_type_ids = mm_token_type_ids.to(device)

    is_vision = (mm_token_type_ids == 1) | (mm_token_type_ids == 2)
    is_prev_vision = torch.roll(is_vision, shifts=1, dims=-1)
    is_prev_vision[..., 0] = False
    new_vision_starts = is_vision & ~is_prev_vision
    vision_group_ids = torch.cumsum(new_vision_starts.int(), dim=1) - 1
    block_sequence_ids = torch.where(is_vision, vision_group_ids, -1)
    return block_sequence_ids


def get_block_sequence_ids_for_mask(mm_token_type_ids: torch.Tensor, device: torch.device) -> torch.Tensor:
    mm_token_type_ids = mm_token_type_ids.to(device)

    is_vision = (mm_token_type_ids == 1) | (mm_token_type_ids == 2)
    is_prev_vision = torch.roll(is_vision, shifts=1, dims=-1)
    is_prev_vision[..., 0] = False
    new_vision_starts = is_vision & ~is_prev_vision
    vision_group_ids = torch.cumsum(new_vision_starts.int(), dim=1) - 1
    block_sequence_ids = torch.where(is_vision, vision_group_ids, -1)
    return block_sequence_ids

