import os

cwd: str = os.getcwd()

# 模型保存设置
model_path: str = cwd + "/model/my_model.h5"

# redis设置
redis_db = 0
redis_host = "127.0.0.1"
redis_queue_name = "test_message:queue"

# 数据集设置
data_path = cwd + "/mnist.npz"
