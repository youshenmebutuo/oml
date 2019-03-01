from __future__ import absolute_import, division, print_function
from tensorflow import keras
import settings
import os
import redis
import json
import tensorflow as tf
import numpy as np


def redis_init():
    """初始化redis设置"""
    rcon: redis.Redis = redis.StrictRedis(
        host=settings.redis_host, db=settings.redis_db)
    rcon.delete(settings.redis_queue_name)
    return rcon


def save_test_data(rcon: redis.Redis, trained_num: int, loss: float, acc: float):
    """保存测试数据"""
    test_message = {"x": str(trained_num), "y_loss": str(
        loss), "y_acc": str(acc)}
    test_message = json.dumps(test_message)
    rcon.lpush(settings.redis_queue_name, test_message)


def load_data(path: str):
    """加载数据集"""
    with np.load(path) as f:
        x_train, y_train = f['x_train'], f['y_train']
        x_test, y_test = f['x_test'], f['y_test']
        x_train = x_train.reshape(-1, 28 * 28) / 255.0
        x_test = x_test.reshape(-1, 28 * 28) / 255.0
        return (x_train, y_train), (x_test, y_test)


def create_model():
    """创建模型"""
    new_model = tf.keras.models.Sequential(
        [keras.layers.Dense(512, activation=tf.nn.relu, input_shape=(784,)), keras.layers.Dropout(0.2),
         keras.layers.Dense(
             256, activation=tf.nn.relu), keras.layers.Dropout(0.4),
         keras.layers.Dense(10, activation=tf.nn.softmax)])
    new_model.compile(optimizer=tf.keras.optimizers.Adam(), loss=tf.keras.losses.sparse_categorical_crossentropy,
                      metrics=['accuracy'])
    return new_model


def train_model(model: keras.Model, train_x, train_y, load_model: bool = False, save_model: bool = False, model_path: str = settings.model_path):
    """训练神经网络模型"""
    if load_model:
        model = keras.models.load_model(model_path)
    model.fit(train_x, train_y, epochs=20)
    if save_model:
        model.save(model_path)


def test_model(model: keras.Model, test_x, test_y):
    """测试模型，并返回测试结果的json字符串"""
    loss, acc = model.evaluate(test_x, test_y)
    return (loss, acc)


def test():
    """测试"""
    # 加载数据
    (train_images, train_labels), (test_images,
                                   test_labels) = load_data(path='mnist.npz')
    # 创建模型
    model = create_model()
    # 训练模型
    train_model(model, train_images, train_labels)
    # 测试模型
    loss, acc = test_model(model, test_images, test_labels)
    # 打印结果
    print("loss:" + str(loss) + "   acc:" + str(acc))


if __name__ == '__main__':
    test()
