
def encoder_shape_dict(batch_size: int, height: int, width: int) -> Mapping[str, list[int]]:
    assert height == 1024 and width == 1024, "Only 1024x1024 images are supported."
    return {
        "image": [batch_size, 3, height, width],
        "image_features_0": [batch_size, 32, height // 4, width // 4],
        "image_features_1": [batch_size, 64, height // 8, width // 8],
        "image_embeddings": [batch_size, 256, height // 16, width // 16],
    }

