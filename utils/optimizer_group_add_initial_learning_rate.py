
def OptimizerGroupAddInitialLearningRate(builder, initialLearningRate):
    builder.PrependFloat32Slot(2, initialLearningRate, 0.0)

