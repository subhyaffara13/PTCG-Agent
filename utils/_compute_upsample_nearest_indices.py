
def _compute_upsample_nearest_indices(input, output_size, scales, exact=False):
    # For each dim in output_size, compute the set of input indices used
    # to produce the upsampled output.
    indices = []
    num_spatial_dims = len(output_size)
    offset = 0.5 if exact else 0.0

    for d in range(num_spatial_dims):
        # Math matches aten/src/ATen/native/cpu/UpSampleKernel.cpp
        #
        # Indices are computed as following:
        # scale = isize / osize
        # Case: exact=False
        # input_index = floor(output_index * scale)
        # Same as OpenCV INTER_NEAREST
        #
        # Case: exact=False
        # index_f32 = (output_index + 0.5) * scale - 0.5
        # input_index = round(index_f32)
        # Same as Pillow and Scikit-Image/Scipy ndi.zoom
        osize = output_size[d]
        isize = input.shape[-num_spatial_dims + d]

        # check for scales[d] > 0 is in compute_scales_value in aten/src/ATen/native/UpSample.h
        scale = (
            isize / (isize * scales[d])
            if scales[d] is not None and scales[d] > 0
            else isize / osize
        )

        output_indices = torch.arange(osize, dtype=torch.float32, device=input.device)
        input_indices = ((output_indices + offset) * scale).to(torch.int64)
        for _ in range(num_spatial_dims - 1 - d):
            input_indices = input_indices.unsqueeze(-1)
        indices.append(input_indices)
    return indices

