
def original_to_transformed_w_coords(original_coords, scale_w):
    return np.round(original_coords * scale_w).astype(np.int32)

