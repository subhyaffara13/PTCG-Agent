import json

def create_dot_product_attention_fp8_backend_config(
    batch, num_heads, seq_q, seq_kv, dtype, fmha_scale, mask_type, layout, is_bwd):
  backend_config = create_dot_product_attention_backend_config_base(
      batch, num_heads, seq_q, seq_kv, dtype, fmha_scale, mask_type, layout, is_bwd)
  return json.dumps(backend_config)

