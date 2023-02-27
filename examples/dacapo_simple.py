import daisy
# print(daisy.__version__)
import dacapo
import logging
import torch
from funlib.geometry import Coordinate

logging.basicConfig(level=logging.INFO)

# 1 data split
from dacapo.experiments.datasplits import TrainValidateDataSplitConfig
from dacapo.experiments.datasplits.datasets import RawGTDatasetConfig
from dacapo.experiments.datasplits.datasets.arrays import ZarrArrayConfig

# change it to versioned Zarr array
train_raw_conf = ZarrArrayConfig(
    "train_raw",
    file_name="/Volumes/cellmap/data/jrc_mus-liver-zon-1/jrc_mus-liver-zon-1.n5",
    dataset="em/fibsem-uint8/s2",
)
train_gt_conf = ZarrArrayConfig(
    "train_gt",
    file_name="/Volumes/cellmap/pattonw/data/tmp_data/jrc_mus-liver-zon-1/jrc_mus-liver-zon-1.n5",
    dataset="volumes/groundtruth/crop344/labels/cells",
)
train_dataset_conf = RawGTDatasetConfig(
    "train_dataset", raw_config=train_raw_conf, gt_config=train_gt_conf
)

val_raw_conf = ZarrArrayConfig(
    "val_raw",
    file_name="/Volumes/cellmap/data/jrc_mus-liver-zon-1/jrc_mus-liver-zon-1.n5",
    dataset="em/fibsem-uint8/s2",
)

val_gt_conf = ZarrArrayConfig(
    "val_gt",
    file_name="/Volumes/cellmap/pattonw/data/tmp_data/jrc_mus-liver-zon-1/jrc_mus-liver-zon-1.n5",
    dataset="volumes/groundtruth/crop344/labels/cells",
)

# mask_config to generate mask to use for training
# mask can be sparse, select region to train on and can use Strategy method to generate mask
val_dataset_conf = RawGTDatasetConfig(
    "val_dataset", raw_config=val_raw_conf, gt_config=val_gt_conf
)

datasplit_conf = TrainValidateDataSplitConfig(
    "test_datasplit",

    train_configs=[train_dataset_conf],
    validate_configs=[val_dataset_conf],
)

# Architecture
from dacapo.experiments.architectures import CNNectomeUNetConfig

architecture_config = CNNectomeUNetConfig(
    name="small_unet",
    input_shape=Coordinate(216, 216, 216),
    eval_shape_increase=Coordinate(72, 72, 72),
    fmaps_in=1,  # one input channel
    num_fmaps=8,  # number feature map
    fmaps_out=32,
    fmap_inc_factor=4,
    # in basic unet they double everytime they down-sample
    downsample_factors=[(2, 2, 2), (2, 2, 2), (2, 2, 2)],
    constant_upsample=True,
)

# task
from dacapo.experiments.tasks import AffinitiesTaskConfig

# loss function
task_config = AffinitiesTaskConfig(
    name="AffinitiesPrediction",
    lsds=False,
    neighborhood=[(0, 0, 1), (0, 1, 0), (1, 0, 0)]
    #     define output channels, here 3 channels
)

#  4 trainer
# hyper parameters / data augmentation
from dacapo.experiments.trainers import GunpowderTrainerConfig
from dacapo.experiments.trainers.gp_augments import (
    SimpleAugmentConfig,
    ElasticAugmentConfig,
    IntensityAugmentConfig,
)
import math
# spacial sampling strategy

trainer_config = GunpowderTrainerConfig(
    name="gunpowder",
    batch_size=2,
    learning_rate=0.0001,
    augments=[
        SimpleAugmentConfig(),
        ElasticAugmentConfig(
            control_point_spacing=(100, 100, 100),
            control_point_displacement_sigma=(10.0, 10.0, 10.0),
            rotation_interval=(0, math.pi / 2.0),
            subsample=8,
            uniform_3d_rotation=True,
        ),
        IntensityAugmentConfig(
            scale=(0.25, 1.75),
            shift=(-0.5, 0.35),
            clip=False,
        )
    ],
    num_data_fetchers=20,
    snapshot_interval=10000,
    min_masked=0.15,
    # min_labelled=0.1,
)

from funlib.geometry import Coordinate
from dacapo.experiments.run_config import RunConfig
from dacapo.experiments.run import Run

run_config = RunConfig(
    name="tutorial_run",
    task_config=task_config,
    architecture_config=architecture_config,
    trainer_config=trainer_config,
    datasplit_config=datasplit_conf,
    repetition=0,
    num_iterations=100000,
    validation_interval=1000,
)
# number of iterations, validation after 1000


run = Run(run_config)

# if you want a summary of the model you can print that here
print(torch.summary(run.model, (1, 216, 216, 216)))

# prediction using model
# run.model