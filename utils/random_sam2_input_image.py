
def random_sam2_input_image(batch_size=1, image_height=1024, image_width=1024) -> torch.Tensor:
    image = torch.randn(batch_size, 3, image_height, image_width, dtype=torch.float32).cpu()
    return image

