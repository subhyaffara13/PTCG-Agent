from typing import Any, List, Optional, Tuple, Union

def launch_func(async_token: _Optional[_ods_ir.Type], async_dependencies: _Sequence[_ods_ir.Value], kernel: _Union[str, _ods_ir.SymbolRefAttr], grid_size_x: _ods_ir.Value, grid_size_y: _ods_ir.Value, grid_size_z: _ods_ir.Value, block_size_x: _ods_ir.Value, block_size_y: _ods_ir.Value, block_size_z: _ods_ir.Value, kernel_operands: _Sequence[_ods_ir.Value], *, cluster_size_x: _Optional[_ods_ir.Value] = None, cluster_size_y: _Optional[_ods_ir.Value] = None, cluster_size_z: _Optional[_ods_ir.Value] = None, dynamic_shared_memory_size: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, cooperative: _Optional[bool] = None, async_object: _Optional[_ods_ir.Value] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, LaunchFuncOp]:
  op = LaunchFuncOp(asyncToken=async_token, asyncDependencies=async_dependencies, kernel=kernel, gridSizeX=grid_size_x, gridSizeY=grid_size_y, gridSizeZ=grid_size_z, blockSizeX=block_size_x, blockSizeY=block_size_y, blockSizeZ=block_size_z, kernelOperands=kernel_operands, clusterSizeX=cluster_size_x, clusterSizeY=cluster_size_y, clusterSizeZ=cluster_size_z, dynamicSharedMemorySize=dynamic_shared_memory_size, cooperative=cooperative, asyncObject=async_object, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def launch_func(
    kernel: List[str],
    grid_size: Tuple[Any, Any, Any],
    block_size: Tuple[Any, Any, Any],
    kernel_operands: Optional[List[Value]] = None,
    async_dependencies: Optional[List[Value]] = None,
    dynamic_shared_memory_size: Optional[Value] = None,
    async_object=None,
    cluster_size: Optional[Tuple[Any, Any, Any]] = None,
    *,
    loc=None,
    ip=None,
) -> Union[Value, List[Value], LaunchFuncOp]:
    op = LaunchFuncOp(
        kernel=kernel,
        grid_size=grid_size,
        block_size=block_size,
        kernel_operands=kernel_operands,
        async_dependencies=async_dependencies,
        dynamic_shared_memory_size=dynamic_shared_memory_size,
        async_object=async_object,
        cluster_size=cluster_size,
        loc=loc,
        ip=ip,
    )
    results = op.results
    if len(results) == 1:
        return results[0]
    elif len(results) > 1:
        return results
    else:
        return op

