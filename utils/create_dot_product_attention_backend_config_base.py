
def create_dot_product_attention_backend_config_base(
    batch, num_heads, seq_q, seq_kv, dtype, fmha_scale, mask_type, layout, is_bwd
):
  # Q, K, V: query, key, value in shape of BT(S)NH or BNT(S)H
  # P: BMM1 output in shape of BNTS
  # O: BMM2 output in the same shape with Q
  # BMM1: Q @ K -> P
  # BMM2: P @ V -> O
  # BMM1Grad1: dP @ Q -> dK
  # BMM1Grad2: dP @ K -> dQ
  # BMM2Grad1: P @ dO -> dV
  # BMM2Grad2: dO @ V -> dP
  cudnn_fmha_backend_config = {
    "algorithm": {
      "algo_id": "0",
      "math_type": "TENSOR_OP_MATH",
      "tuning_knobs": {"17": "1", "24": "0"},
      "is_cudnn_frontend": True,
      "workspace_size": "0",
    },
    "fmha_scale": fmha_scale,
    "intermediate_tensor_shape": {
      "element_type": element_type_to_backend_config_type_mapping(dtype),
      "dimensions": [str(batch), str(num_heads), str(seq_q), str(seq_kv)],
      "tuple_shapes": [],
      "layout": {
        "dim_level_types": [],
        "dim_unique": [],
        "dim_ordered": [],
        "minor_to_major": ["3", "2", "1", "0"],
        "tiles": [],
        "element_size_in_bits": "0",
        "memory_space": "0",
        "index_primitive_type": "PRIMITIVE_TYPE_INVALID",
        "pointer_primitive_type": "PRIMITIVE_TYPE_INVALID",
        "dynamic_shape_metadata_prefix_bytes": "0",
      },
      "is_dynamic_dimension": [False, False, False, False],
    },
    "is_flash_attention": True,
    "mask_type": convert_mask_type_to_string(mask_type),
  }

  # We define the contracting and batch dims in the format of
  # ((lhs_contracting_dims, rhs_contracting_dims), (lhs_batch_dims,
  # rhs_batch_dims)).
  if layout == AttentionLayout.BNTH.value:
    dims = [
        ((3, 3), ((0, 1), (0, 1))), # BMM1: BNTH,BNSH->BNTS
        ((3, 2), ((0, 1), (0, 1))), # BMM2: BNTS,BNSH->BNTH
        ((2, 2), ((0, 1), (0, 1))), # BMM1_grad_1: BNTS,BNTH->BNSH
        ((3, 2), ((0, 1), (0, 1))), # BMM1_grad_2: BNTS,BNSH->BNTH
        ((2, 2), ((0, 1), (0, 1))), # BMM2_grad_1: BNTS,BNTH->BNSH
        ((3, 3), ((0, 1), (0, 1))), # BMM2_grad_2: BNTH,BNSH->BNTS
    ]
  else:
    dims = [
        ((3, 3), ((0, 2), (0, 2))), # BMM1: BTNH,BSNH->BNTS
        ((3, 1), ((0, 1), (0, 2))), # BMM2: BNTS,BSNH->BTNH
        ((2, 1), ((0, 1), (0, 2))), # BMM1_grad_1: BNTS,BTNH->BSNH
        ((3, 1), ((0, 1), (0, 2))), # BMM1_grad_2: BNTS,BSNH->BTNH
        ((2, 1), ((0, 1), (0, 2))), # BMM2_grad_1: BNTS,BTNH->BSNH
        ((3, 3), ((0, 2), (0, 2))), # BMM2_grad_2: BTNH,BSNH->BNTS
    ]
  keys = [
      "bmm1_dot_dimension_numbers",
      "bmm2_dot_dimension_numbers",
      "bmm1_grad_gemm1_dot_dimension_numbers",
      "bmm1_grad_gemm2_dot_dimension_numbers",
      "bmm2_grad_gemm1_dot_dimension_numbers",
      "bmm2_grad_gemm2_dot_dimension_numbers",
  ]
  fwd_dot_number = {}
  bwd_dot_number = {}
  for idx, (key, ((lc, rc), (lb, rb))) in enumerate(zip(keys, dims)):
    dims_to_write = fwd_dot_number if idx < 2 else bwd_dot_number
    dims_to_write[key] = {
        "lhs_contracting_dimensions": [str(lc)],
        "rhs_contracting_dimensions": [str(rc)],
        "lhs_batch_dimensions": [str(i) for i in lb],
        "rhs_batch_dimensions": [str(i) for i in rb],
    }

  if is_bwd:
    cudnn_fmha_backend_config = {**cudnn_fmha_backend_config, **bwd_dot_number}
  else:
    cudnn_fmha_backend_config = {**cudnn_fmha_backend_config, **fwd_dot_number}
  backend_config = {
    "operation_queue_id":"0",
    "cudnn_fmha_backend_config": cudnn_fmha_backend_config
  }
  return backend_config

