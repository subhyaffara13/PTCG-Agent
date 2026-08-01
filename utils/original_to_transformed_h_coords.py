
def original_to_transformed_h_coords(original_coords, scale_h):
    return np.round(original_coords * scale_h).astype(np.int32)

