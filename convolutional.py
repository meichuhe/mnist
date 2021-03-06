#!/usr/bin/env python
# coding: utf-8

# In[2]:


# coding: utf-8
import os

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


# In[7]:


mnist = input_data.read_data_sets("MNIST_data/",one_hot=True)
x = tf.placeholder(tf.float32,[None, 784])
y_ = tf.placeholder(tf.float32,[None, 10])


# In[9]:


# 将单张图片从784维向量还原为28x28的矩阵图片
x_image = tf.reshape(x,[-1,28,28,1])


# In[11]:


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


# In[13]:


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


# In[16]:


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding=                       'SAME')


# In[18]:


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides                         =[1,2,2,1], padding='SAME')


# In[20]:


# 第一层卷积
W_conv1 = weight_variable([5,5,1,32])
b_conv1 = bias_variable([32])
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1)+b_conv1)
h_pool1 = max_pool_2x2(h_conv1)


# In[22]:


# 第二层卷积层
W_conv2 = weight_variable([5,5,32,64])
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2)+b_conv2)
h_pool2 = max_pool_2x2(h_conv2)


# In[27]:


# 全连接层，输出1024维向量
W_fc1 = weight_variable([7*7*64,1024])
b_fc1 = bias_variable([1024])
h_pool2_flat = tf.reshape(h_pool2, [-1,7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1)                  + b_fc1)
# 使用Dropout, keep_prob是一个占位符，训练时为0.5，测试时为1
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop= tf.nn.dropout(h_fc1,keep_prob)


# In[30]:


# 把1024维向量转换成10维，对应10个类别
W_fc2 = weight_variable([1024,10])
b_fc2 = bias_variable([10])
y_conv = tf.matmul(h_fc1_drop, W_fc2)+b_fc2


# In[35]:


# 不采用先softmax再计算交叉熵的方法
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_,logits=y_conv))
# 定义train_step
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)


# In[40]:


# 定义测试的准确率
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


# In[ ]:

config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.8
# 程序最多只能占用指定gpu50%的显存
config.gpu_options.allow_growth = True      #程序按需申请内存
# sess = tf.Session(config = config)

sess = tf.InteractiveSession(config=config)
sess.run(tf.global_variables_initializer())

for i in range(20000):
    batch = mnist.train.next_batch(50)
    if i % 100 == 0:
        train_accuracy = accuracy.eval(feed_dict={
            x: batch[0], y_:batch[1], keep_prob:1.0
        })
        print("step %d, training accuracy %g" % (i, train_accuracy))
    train_step.run(feed_dict={x:batch[0], y_:batch[1], keep_prob:0.5})


# In[ ]:


print("test accuracy %g" % accuracy.eval(feed_dict={
    x:mnist.test.images, y_:mnist.test.labels, keep_prob:1.0
}))

