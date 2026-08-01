
def _static_reference_quantized_linear_module(N, K, bias, example_input):
    """
    Generate a linear module with quantize-dequantize (reference quantized)
    with static quantization parameters (no choose_qparams at runtime).
    A simulation to PT2E quantization in Torchao.
    It is used to test fusion and lowering passes in Inductor for X86 CPU.
    Input quantization limit is 0-127 to avoid overflow on old platforms.
    Params:
        N: output feature dimension
        K: input feature dimension
        bias: boolean flag to indicate whether linear module has bias
        example_input: example input tensor to get scale/zero point
    Return:
        An instance of the reference quantized linear module
    """
    class Model(torch.nn.Module):
        def __init__(self, N, K, bias, example_input):
            super().__init__()
            self.x_scale, self.x_zp = torch.ops.quantized_decomposed.choose_qparams.tensor(
                example_input,
                quant_min=0,
                quant_max=127,
                eps=torch.finfo(torch.float32).eps,
                dtype=torch.uint8,
            )
            self.x_scale, self.x_zp = self.x_scale.detach().item(), self.x_zp.detach().item()
            self.linear = torch.nn.Linear(K, N, bias)
            self.w_scales, self.w_zps = torch.ops.quantized_decomposed.choose_qparams_per_token(
                self.linear.weight, dtype=torch.int8
            )
            self.w_scales = self.w_scales.detach().to(torch.float32).squeeze()
            self.w_zps = self.w_zps.detach().to(torch.int64).squeeze()
            self.qw = torch.ops.quantized_decomposed.quantize_per_channel.default(
                self.linear.weight,
                self.w_scales,
                self.w_zps,
                axis=0,
                quant_min=-128,
                quant_max=127,
                dtype=torch.int8,
            )

        def forward(self, x):
            dqw = torch.ops.quantized_decomposed.dequantize_per_channel.default(
                self.qw,
                self.w_scales,
                self.w_zps,
                axis=0,
                quant_min=-128,
                quant_max=127,
                dtype=torch.int8,
            )
            quantize_per_tensor_default = torch.ops.quantized_decomposed.quantize_per_tensor.default(
                x,
                self.x_scale,
                self.x_zp,
                quant_min=0,
                quant_max=127,
                dtype=torch.uint8,
            )
            dequantize_per_tensor_default = torch.ops.quantized_decomposed.dequantize_per_tensor.default(
                quantize_per_tensor_default,
                self.x_scale,
                self.x_zp,
                quant_min=0,
                quant_max=127,
                dtype=torch.uint8,
            )
            linear = torch.ops.aten.linear.default(dequantize_per_tensor_default, dqw, self.linear.bias)
            return linear

    return Model(N, K, bias, example_input).eval()

