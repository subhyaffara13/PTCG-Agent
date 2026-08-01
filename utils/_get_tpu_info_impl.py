
def _get_tpu_info_impl(chip_version: ChipVersion, num_cores: int) -> TpuInfo:
  """Returns the TPU hardware info for the given chip version and core count.

  Note that all information is *per-TensorCore* so you would need to multiply by
  `num_cores` to obtain the total for the chip.

  Args:
    chip_version: The TPU chip version.
    num_cores: The number of TensorCores per chip for this configuration. This
      is influenced by the TPU version and whether Megacore is enabled.
  """
  # Common parameters for all TensorCores
  NUM_LANES = 128
  NUM_SUBLANES = 8
  MXU_COLUMN_SIZE_GEN_LT_6 = 128
  MXU_COLUMN_SIZE_GEN_GE_6 = 256
  tensor_cores_per_chip = chip_version.num_physical_tensor_cores_per_chip
  match chip_version:
    case ChipVersion.TPU_V2:
      return TpuInfo(
          chip_version=chip_version,
          generation=2,
          num_cores=num_cores,
          num_lanes=NUM_LANES,
          num_sublanes=NUM_SUBLANES,
          mxu_column_size=MXU_COLUMN_SIZE_GEN_LT_6,
          num_mxus=1,
          num_accumulators=0,  # Not Available
          vmem_capacity_bytes=16 * 1024 * 1024,  # 16 MiB per core
          cmem_capacity_bytes=0,
          smem_capacity_bytes=16 * 1024,  # 16 KiB per core
          hbm_capacity_bytes=int(16_000_000_000 // tensor_cores_per_chip),
          mem_bw_bytes_per_second=int(7.16e11 // tensor_cores_per_chip),
          bf16_ops_per_second=int(4.6e13 // tensor_cores_per_chip),
          int8_ops_per_second=0,  # Not Available
          fp8_ops_per_second=0,  # Not Available
          int4_ops_per_second=0,  # Not Available
      )
    case ChipVersion.TPU_V3:
      return TpuInfo(
          chip_version=chip_version,
          generation=3,
          num_cores=num_cores,
          num_lanes=NUM_LANES,
          num_sublanes=NUM_SUBLANES,
          mxu_column_size=MXU_COLUMN_SIZE_GEN_LT_6,
          num_mxus=2,
          num_accumulators=0,  # Not Available
          vmem_capacity_bytes=16 * 1024 * 1024,  # 16 MiB per core
          cmem_capacity_bytes=0,
          smem_capacity_bytes=16 * 1024,  # 16 KiB per core
          hbm_capacity_bytes=34_400_000_000 // tensor_cores_per_chip,
          mem_bw_bytes_per_second=int(8.25e11 // tensor_cores_per_chip),
          bf16_ops_per_second=int(1.40e14 // tensor_cores_per_chip),
          int8_ops_per_second=0,  # Not Available
          fp8_ops_per_second=0,  # Not Available
          int4_ops_per_second=0,  # Not Available
      )
    case ChipVersion.TPU_V4I:
      return TpuInfo(
          chip_version=chip_version,
          generation=4,
          num_cores=num_cores,
          num_lanes=NUM_LANES,
          num_sublanes=NUM_SUBLANES,
          mxu_column_size=MXU_COLUMN_SIZE_GEN_LT_6,
          num_mxus=4,
          num_accumulators=0,  # Not Available
          vmem_capacity_bytes=16 * 1024 * 1024,  # 16 MiB per core
          cmem_capacity_bytes=134_000_000,
          smem_capacity_bytes=1024 * 1024,  # 1 MiB per core
          hbm_capacity_bytes=8_590_000_000,
          mem_bw_bytes_per_second=int(6.14e11),
          bf16_ops_per_second=int(1.37e14),
          int8_ops_per_second=0,  # Not Available
          fp8_ops_per_second=0,  # Not Available
          int4_ops_per_second=0,  # Not Available
      )
    case ChipVersion.TPU_V4:
      return TpuInfo(
          chip_version=chip_version,
          generation=4,
          num_cores=num_cores,
          num_lanes=NUM_LANES,
          num_sublanes=NUM_SUBLANES,
          mxu_column_size=MXU_COLUMN_SIZE_GEN_LT_6,
          num_mxus=4,
          num_accumulators=0,  # Not Available
          vmem_capacity_bytes=16 * 1024 * 1024,  # 16 MiB per core
          cmem_capacity_bytes=134_000_000 // tensor_cores_per_chip,
          smem_capacity_bytes=1024 * 1024,  # 1 MiB per core
          hbm_capacity_bytes=34_400_000_000 // tensor_cores_per_chip,
          mem_bw_bytes_per_second=int(1.23e12 // tensor_cores_per_chip),
          bf16_ops_per_second=int(2.75e14 // tensor_cores_per_chip),
          int8_ops_per_second=0,  # Not Available
          fp8_ops_per_second=0,  # Not Available
          int4_ops_per_second=0,  # Not Available
      )
    case ChipVersion.TPU_V5E:
      return TpuInfo(
          chip_version=chip_version,
          generation=5,
          num_cores=num_cores,
          num_lanes=NUM_LANES,
          num_sublanes=NUM_SUBLANES,
          mxu_column_size=MXU_COLUMN_SIZE_GEN_LT_6,
          num_mxus=4,
          num_accumulators=0,  # Not Available
          vmem_capacity_bytes=128 * 1024 * 1024,  # 128 MiB per core
          cmem_capacity_bytes=0,
          smem_capacity_bytes=1024 * 1024,  # 1 MiB per core
          hbm_capacity_bytes=17_200_000_000,
          mem_bw_bytes_per_second=int(8.20e11),
          bf16_ops_per_second=int(1.97e14),
          int8_ops_per_second=int(3.94e14),
          fp8_ops_per_second=0,  # Not Available
          int4_ops_per_second=int(7.88e14),
      )
    case ChipVersion.TPU_V5P:
      return TpuInfo(
          chip_version=chip_version,
          generation=5,
          num_cores=num_cores,
          num_lanes=NUM_LANES,
          num_sublanes=NUM_SUBLANES,
          mxu_column_size=MXU_COLUMN_SIZE_GEN_LT_6,
          num_mxus=4,
          num_accumulators=0,  # Not Available
          vmem_capacity_bytes=64 * 1024 * 1024,  # 64 MiB per core
          cmem_capacity_bytes=0,
          smem_capacity_bytes=1024 * 1024,  # 1 MiB per core
          hbm_capacity_bytes=103_000_000_000 // tensor_cores_per_chip,
          mem_bw_bytes_per_second=int(2.46e12 // tensor_cores_per_chip),
          bf16_ops_per_second=int(4.59e14 // tensor_cores_per_chip),
          int8_ops_per_second=int(9.18e14 // tensor_cores_per_chip),
          fp8_ops_per_second=0,  # Not Available
          int4_ops_per_second=int(1.84e15 // tensor_cores_per_chip),
          sparse_core=SparseCoreInfo(
              num_cores=4,
              num_subcores=16,
              num_lanes=8,
              vmem_capacity_bytes=512 * 1024,  # 512 KiB per vector subcore
              dma_granule_size_bytes=32,
          ),
      )
    case ChipVersion.TPU_V6E:
      return TpuInfo(
          chip_version=chip_version,
          generation=6,
          num_cores=num_cores,
          num_lanes=NUM_LANES,
          num_sublanes=NUM_SUBLANES,
          mxu_column_size=MXU_COLUMN_SIZE_GEN_GE_6,
          num_mxus=2,
          num_accumulators=0,  # Not Available
          vmem_capacity_bytes=128 * 1024 * 1024,  # 128 MiB per core
          cmem_capacity_bytes=0,
          smem_capacity_bytes=1024 * 1024,  # 1 MiB per core
          hbm_capacity_bytes=34_400_000_000,
          mem_bw_bytes_per_second=int(1.64e12),
          bf16_ops_per_second=int(9.20e14),
          int8_ops_per_second=int(1.84e15),
          fp8_ops_per_second=int(9.20e14),
          int4_ops_per_second=int(3.68e15),
          sparse_core=SparseCoreInfo(
              num_cores=2,
              num_subcores=16,
              num_lanes=8,
              vmem_capacity_bytes=256 * 1024,  # 256 KiB per vector subcore
              dma_granule_size_bytes=32,
          ),
      )
    case ChipVersion.TPU_7 | ChipVersion.TPU_7X:
      return TpuInfo(
          chip_version=chip_version,
          generation=7,
          num_cores=num_cores,
          num_lanes=128,
          num_sublanes=8,
          mxu_column_size=256,
          num_mxus=2,
          num_accumulators=128,
          vmem_capacity_bytes=64 * 1024 * 1024,  # 64 MiB per core
          cmem_capacity_bytes=0,
          smem_capacity_bytes=1024 * 1024,  # 1 MiB per core
          hbm_capacity_bytes=206_000_000_000 // tensor_cores_per_chip,
          mem_bw_bytes_per_second=int(7.40e12 // tensor_cores_per_chip),
          bf16_ops_per_second=int(2.31e15 // tensor_cores_per_chip),
          int8_ops_per_second=0,  # Not Available
          fp8_ops_per_second=int(4.60e15 // tensor_cores_per_chip),
          int4_ops_per_second=0,  # Not Available
          sparse_core=SparseCoreInfo(
              num_cores=2,
              num_subcores=16,
              num_lanes=16,
              vmem_capacity_bytes=512 * 1024,  # 512 KiB per vector subcore
              dma_granule_size_bytes=32,
          ),
      )
    case ChipVersion.TPU_8I:
      return TpuInfo(
          chip_version=chip_version,
          generation=8,
          num_cores=num_cores,
          num_lanes=128,
          num_sublanes=8,
          mxu_column_size=256,
          num_mxus=2,
          num_accumulators=256,
          vmem_capacity_bytes=192 * 1024 * 1024,  # 192 MiB per core
          cmem_capacity_bytes=0,
          smem_capacity_bytes=1024 * 1024,  # 1 MiB per core
          hbm_capacity_bytes=309_000_000_000 // tensor_cores_per_chip,
          mem_bw_bytes_per_second=int(8.60e12 // tensor_cores_per_chip),
          bf16_ops_per_second=int(1.101e15 // tensor_cores_per_chip),
          int8_ops_per_second=0,  # Not Available
          fp8_ops_per_second=int(8.808e15 // tensor_cores_per_chip),
          int4_ops_per_second=0,  # Not Available
          sparse_core=SparseCoreInfo(
              num_cores=1,
              num_subcores=4,
              num_lanes=16,
              vmem_capacity_bytes=512 * 1024,  # 512 KiB per vector subcore
              dma_granule_size_bytes=64,
          ),
      )
    case _:
      raise ValueError(f"Unsupported TPU chip version: {chip_version}")

