
def decoder_shape_dict(
    original_image_height: int,
    original_image_width: int,
    num_labels: int = 1,
    max_points: int = 16,
    num_masks: int = 1,
) -> dict:
    height: int = 1024
    width: int = 1024
    return {
        "image_features_0": [1, 32, height // 4, width // 4],
        "image_features_1": [1, 64, height // 8, width // 8],
        "image_embeddings": [1, 256, height // 16, width // 16],
        "point_coords": [num_labels, max_points, 2],
        "point_labels": [num_labels, max_points],
        "input_masks": [num_labels, 1, height // 4, width // 4],
        "has_input_masks": [num_labels],
        "original_image_size": [2],
        "masks": [num_labels, num_masks, original_image_height, original_image_width],
        "iou_predictions": [num_labels, num_masks],
        "low_res_masks": [num_labels, num_masks, height // 4, width // 4],
    }

