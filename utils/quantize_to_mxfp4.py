
def quantize_to_mxfp4(w, triton_kernels_hub):
    downcast_to_mxfp_torch = triton_kernels_hub.numerics_details.mxfp.downcast_to_mxfp_torch
    w, w_scale = downcast_to_mxfp_torch(w.to(torch.bfloat16), torch.uint8, axis=1)
    return w, w_scale

