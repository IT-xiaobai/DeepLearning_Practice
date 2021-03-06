#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : Kerr
@License : Copyright(C) 2018, Get
@Contact : 905392619@qq.com
@Software: PyCharm
@File    : mnist_with_CNN.py
@Time    : 2018-09-17 18:49
@Desc    : 基于CNN的mnist手写体识别，准确率0.9911
"""
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import os
import time

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


def get_lapse_time(start_time, end_time):
    """
    格式化时间，可用于计算程序运行时间
    :param start_time: 开始时间
    :param end_time: 结束时间
    :return: 时分秒显示
    """
    start_num = 3600 * int(start_time[:2]) + 60 * int(start_time[2:4]) + int(start_time[-2:])
    end_num = 3600 * int(end_time[:2]) + 60 * int(end_time[2:4]) + int(end_time[-2:])
    hours = (end_num - start_num) // 3600
    minutes = ((end_num - start_num) % 3600) // 60
    seconds = ((end_num - start_num) % 3600) % 60
    gap_time = "%02d:%02d:%02d" % (hours, minutes, seconds)
    return gap_time


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


if __name__ == '__main__':
    start = time.strftime("%H %M %S")
    sess = tf.InteractiveSession()
    # config = tf.ConfigProto()
    # config.gpu_options.allow_growth = True
    # sess = tf.Session(config=config)

    mnist = input_data.read_data_sets("./MNIST_data", one_hot=True)
    x = tf.placeholder(tf.float32, shape=[None, 784])
    y_ = tf.placeholder(tf.float32, shape=[None, 10])
    x_image = tf.reshape(x, [-1, 28, 28, 1])

    # The first convolutional layer
    W_conv1 = weight_variable([5, 5, 1, 32])
    b_conv1 = bias_variable([32])
    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    # The second Convolutional layer
    W_conv2 = weight_variable([5, 5, 32, 64])
    b_conv2 = bias_variable([64])
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

    # Fully connected layer
    W_fc1 = weight_variable([7 * 7 * 64, 1024])
    b_fc1 = bias_variable([1024])
    h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    # Dropout
    keep_prob = tf.placeholder("float")
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    # Output layer
    W_fc2 = weight_variable([1024, 10])
    b_fc2 = bias_variable([10])
    y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

    # train
    cross_entropy = -tf.reduce_sum(y_ * tf.log(y_conv))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    sess.run(tf.global_variables_initializer())
    train_start = time.strftime("%H %M %S")
    for i in range(20000):
        batch = mnist.train.next_batch(50)
        if i % 100 == 0:
            train_accuracy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
            print("step %d, training accuracy %g" % (i, train_accuracy))
        train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
    train_end = time.strftime("%H %M %S")

    # test
    print("test accuracy %g" % accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))
    end = time.strftime("%H %M %S")
    print("训练用时：%s" % get_lapse_time(train_start, train_end))
    print("程序运行用时：%s" % get_lapse_time(start, end))
