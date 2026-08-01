
def get_gemm_template_output_and_compute_dtype(input_dtype):
    if input_dtype in [torch.uint8, torch.int8]:
        return (torch.int32, torch.int32)
    else:
        return (torch.float32, torch.float32)

