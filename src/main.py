import oml_function as oml
import random
import settings
import json


def run():
    """使用批量增量训练法来模拟在线学习过程"""
    rcon = oml.redis_init()
    # 加载数据集
    (train_images, train_labels), (test_images,
                                   test_labels) = oml.load_data(path=settings.data_path)
    model = oml.create_model()
    train_set_size = len(train_labels)
    # train_set_size = 1000
    trained_num = 0
    loss, acc = oml.test_model(model, test_images, test_labels)
    oml.save_test_data(rcon, trained_num, loss, acc)

    while True:
        batch_size = random.randint(1, 100)
        print("trained_num:" + str(trained_num) +
              "   barch_size:" + str(batch_size))
        if trained_num + batch_size >= train_set_size:
            break
        tmp_train_images = train_images[trained_num: trained_num + batch_size]
        tmp_train_labels = train_labels[trained_num: trained_num + batch_size]
        trained_num += batch_size
        oml.train_model(model, tmp_train_images,
                        tmp_train_labels, save_model=True)
        loss, acc = oml.test_model(model, test_images, test_labels)
        oml.save_test_data(rcon, trained_num, loss, acc)


if __name__ == "__main__":
    run()
