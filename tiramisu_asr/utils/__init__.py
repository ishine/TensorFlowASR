# Copyright 2020 Huy Le Nguyen (@usimarit)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def setup_environment():  # Set memory growth and only log ERRORs
    import os
    import warnings

    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
    warnings.simplefilter("ignore")

    import tensorflow as tf

    tf.get_logger().setLevel("ERROR")

    tf.config.optimizer.set_experimental_options({"auto_mixed_precision": True})


def setup_strategy(devices):
    import tensorflow as tf
    try:
        # Currently, memory growth needs to be the same across GPUs
        gpus = tf.config.list_physical_devices("GPU")
        for gpu in [gpus[i] for i in devices]:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(len(gpus), "Physical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)

    return tf.distribute.MirroredStrategy(devices=[f"/GPU:{i}" for i in devices])


def setup_tpu(tpu_address):
    import tensorflow as tf

    resolver = tf.distribute.cluster_resolver.TPUClusterResolver(tpu='grpc://' + tpu_address)
    tf.config.experimental_connect_to_cluster(resolver)
    tf.tpu.experimental.initialize_tpu_system(resolver)
    print("All TPUs: ", tf.config.list_logical_devices('TPU'))
    return resolver
