# -*- coding: utf-8 -*-
# @Time    : 2020-04-18 18:09
# @Author  : speeding_motor

import config
import data_generator
import matplotlib
import yolo
import time
import tensorflow as tf
matplotlib.use("TkAgg")
from matplotlib import pyplot
from tensorflow import keras
from yolo_loss import YoloLoss


def train():
    batch_image_names, batch_boxs = data_generator.get_batch_data()

    yolo_model = yolo.YoloModel()
    yolo_loss = YoloLoss()
    optimizer = keras.optimizers.Adam(learning_rate=0.1)

    for epoch in range(config.EPOCHS):
        for i in range(batch_image_names.shape[0]//config.BATCH_SIZE):
            batch_labels = data_generator.generate_label_from_box(batch_boxs[i])
            batch_images = data_generator.read_image_from_names(batch_image_names[i])

            # show_image(batch_images[0:config.BATCH_SIZE])
            with tf.GradientTape() as tape:

                batch_prediction = yolo_model(batch_images)

                loss = yolo_loss(batch_labels, batch_prediction)

            grads = tape.gradient(loss, yolo_model.trainable_weights)
            optimizer.apply_gradients(zip(grads, yolo_model.trainable_variables))

            print("epoch ={},i = {} loss={}".format(epoch, i, loss))

    keras.utils.plot_model(yolo_model, to_file='model.png', show_shapes=True, show_layer_names=True,
                               rankdir='LR', expand_nested=False, dpi=96)


def show_image(images):
    pyplot.figure(figsize=(20, 20))
    for i, image in enumerate(images):
        pyplot.subplot(2, 6, i+1)
        pyplot.imshow(images[i].numpy())
        pyplot.xticks([])
        pyplot.yticks([])

    pyplot.show()


if __name__ == '__main__':
    train()
    print("train done spend time {}".format(time.clock()))


