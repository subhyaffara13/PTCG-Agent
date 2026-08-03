from typing import Any

def load_weights_to_pt2_contents(
    pt2_contents: PT2ArchiveContents, weights_map: dict[str, Any]
) -> None:
    """
    Load weights into the models in PT2 archive contents

    Args:
        pt2_contents (PT2ArchiveContents): The contents of the PT2 archive.
    """
    for model_name, weights in weights_map.items():
        if model_name not in pt2_contents.aoti_runners:
            raise RuntimeError(f"Model {model_name} not found in PT2 archive contents.")
        pt2_contents.aoti_runners[model_name].load_constants(
            weights, check_full_update=True, user_managed=True
        )

