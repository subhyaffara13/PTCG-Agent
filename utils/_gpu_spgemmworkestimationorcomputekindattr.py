
def _gpu_spgemmworkestimationorcomputekindattr(x, context):
    return _ods_ir.Attribute.parse(f'#gpu<spgemm_work_estimation_or_compute_kind {str(x)}>', context=context)

