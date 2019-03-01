import os
# 检查点设置
checkpoint_path: str = "/home/yc/VSCode/Python/oml/src/training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# 模型保存设置
model_path: str = "/home/yc/VSCode/Python/oml/src/model/my_model.h5"

# redis设置
redis_db = 0
redis_host = "127.0.0.1"
redis_queue_name = "test_message:queue"

# 数据集设置
data_path = "/home/yc/VSCode/Python/oml/src/mnist.npz"
