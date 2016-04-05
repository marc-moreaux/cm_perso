from __future__ import print_function
import numpy as np
import tensorflow as tf
from six.moves import cPickle as pickle


def reformat(dataset, labels):
  dataset = dataset.reshape((-1, image_size * image_size)).astype(np.float32)
  # Map 2 to [0.0, 1.0, 0.0 ...], 3 to [0.0, 0.0, 1.0 ...]
  labels = (np.arange(num_labels) == labels[:,None]).astype(np.float32)
  return dataset, labels

def accuracy(predictions, labels):
  return (100.0 * np.sum(np.argmax(predictions, 1) == np.argmax(labels, 1))
          / predictions.shape[0])

pickle_file = 'notMNIST.pickle'

with open(pickle_file, 'rb') as f:
  save = pickle.load(f)
  train_dataset = save['train_dataset']
  train_labels = save['train_labels']
  valid_dataset = save['valid_dataset']
  valid_labels = save['valid_labels']
  test_dataset = save['test_dataset']
  test_labels = save['test_labels']
  del save  # hint to help gc free up memory
  print('Training set', train_dataset.shape, train_labels.shape)
  print('Validation set', valid_dataset.shape, valid_labels.shape)
  print('Test set', test_dataset.shape, test_labels.shape)

image_size = 28
num_labels = 10

train_dataset, train_labels = reformat(train_dataset, train_labels)
valid_dataset, valid_labels = reformat(valid_dataset, valid_labels)
test_dataset, test_labels = reformat(test_dataset, test_labels)
print('Training set', train_dataset.shape, train_labels.shape)
print('Validation set', valid_dataset.shape, valid_labels.shape)
print('Test set', test_dataset.shape, test_labels.shape)


#####################################
#        logistic regression
#####################################
batch_size = 128
num_steps = 3001

graph = tf.Graph()
with graph.as_default():
  # Input data. 
  tf_train_dataset = tf.placeholder(tf.float32, shape=(batch_size, image_size * image_size))
  tf_train_labels = tf.placeholder(tf.float32, shape=(batch_size, num_labels))
  tf_valid_dataset = tf.constant(valid_dataset)
  tf_test_dataset = tf.constant(test_dataset)
  isL2 = tf.placeholder(tf.bool)
  
  # Variables.
  weights = tf.Variable(tf.truncated_normal([image_size * image_size, num_labels]))
  biases = tf.Variable(tf.zeros([num_labels]))
  
  # Training computation.
  def prediction(mInput):
    logits = tf.matmul(mInput, weights) + biases
    return logits

  # define loss funtion
  if isL2 :
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(prediction(tf_train_dataset), tf_train_labels) )
  else :
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(prediction(tf_train_dataset), tf_train_labels) + .05*tf.nn.l2_loss(weights))
  
  # Optimizer.
  optimizer = tf.train.GradientDescentOptimizer(0.5).minimize(loss)
  
  # Predictions for the training, validation, and test data.
  train_prediction = tf.nn.softmax( prediction(tf_train_dataset) )
  valid_prediction = tf.nn.softmax( prediction(tf_valid_dataset) )
  test_prediction  = tf.nn.softmax( prediction(tf_test_dataset ) )


with tf.Session(graph=graph) as session:
  tf.initialize_all_variables().run()
  print("Initialized")
  for step in range(num_steps):
    # Pick an offset within the training data, which has been randomized.
    offset = (step * batch_size) % (train_labels.shape[0] - batch_size)
    # Generate a minibatch.
    batch_data = train_dataset[offset:(offset + batch_size), :]
    batch_labels = train_labels[offset:(offset + batch_size), :]
    # Prepare a dictionary telling the session where to feed the minibatch.
    # The key of the dictionary is the placeholder node of the graph to be fed,
    # and the value is the numpy array to feed to it.
    feed_dict = {tf_train_dataset : batch_data, tf_train_labels : batch_labels, isL2 : False}
    _, l, predictions = session.run([optimizer, loss, train_prediction], feed_dict=feed_dict)
    if (step % 500 == 0):
      print("Minibatch loss at step %d: %f" % (step, l))
      print("Minibatch accuracy: %.1f%%" % accuracy(predictions, batch_labels))
      print("Validation accuracy: %.1f%%" % accuracy(valid_prediction.eval(), valid_labels))
  print("Test accuracy: %.1f%%" % accuracy(test_prediction.eval(), test_labels))



#####################################
#    hidden layer neural network 
# with rectified linear units (nn.relu()) 
#       and 1024 hidden nodes
#####################################
batch_size = 128
num_steps = 3001

graph = tf.Graph()
with graph.as_default():
  # Input data. 
  tf_train_dataset = tf.placeholder(tf.float32, shape=(batch_size, image_size * image_size))
  tf_train_labels = tf.placeholder(tf.float32, shape=(batch_size, num_labels))
  tf_valid_dataset = tf.constant(valid_dataset)
  tf_test_dataset = tf.constant(test_dataset)
  
  # Variables.
  weights_h = tf.Variable(tf.truncated_normal([image_size * image_size, 1024]))
  biases_h = tf.Variable(tf.zeros([1024]))
  weights = tf.Variable(tf.truncated_normal([1024, num_labels]))
  biases = tf.Variable(tf.zeros([num_labels]))
  keep_prob = tf.placeholder(tf.float32)
  isDropout = tf.placeholder(tf.bool)
  isL2 = tf.placeholder(tf.bool)
  
  # Training computation.
  def prediction(mInput, dropout=False):
    layer1 = tf.nn.relu(tf.matmul(mInput, weights_h) + biases_h)
    if dropout : layer1 = tf.nn.dropout(layer1, keep_prob)
    logits = tf.matmul(layer1, weights) + biases
    return logits
  
  # Choose on of the loss functions
  if isL2 :
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
           prediction(tf_train_dataset, isDropout), tf_train_labels) )
  else :
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
           prediction(tf_train_dataset, isDropout), tf_train_labels)
           + .01*tf.nn.l2_loss(weights) + .01*tf.nn.l2_loss(weights_h))
  
  # Optimizer.
  global_step = tf.Variable(0)  # count the number of steps taken.
  learning_rate = tf.train.exponential_decay(0.5, global_step, 100000, 0.96) # decay every 100000 steps with a base of 0.96
  optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)
  # optimizer = tf.train.GradientDescentOptimizer(0.5).minimize(loss)
  
  # Predictions for the training, validation, and test data.
  train_prediction = tf.nn.softmax( prediction(tf_train_dataset) )
  valid_prediction = tf.nn.softmax( prediction(tf_valid_dataset) )
  test_prediction  = tf.nn.softmax( prediction(tf_test_dataset ) )



with tf.Session(graph=graph) as session:
  tf.initialize_all_variables().run()
  print("Initialized")
  for step in range(num_steps):
    # Pick an offset within the training data, which has been randomized.
    offset = (step * batch_size) % (train_labels.shape[0] - batch_size)
    # Generate a minibatch.
    batch_data = train_dataset[offset:(offset + batch_size), :]
    batch_labels = train_labels[offset:(offset + batch_size), :]
    # Prepare a dictionary telling the session where to feed the minibatch.
    # The key of the dictionary is the placeholder node of the graph to be fed,
    # and the value is the numpy array to feed to it.
    feed_dict = {tf_train_dataset : batch_data, tf_train_labels : batch_labels, keep_prob: 0.5, isL2:False, isDropout:False}
    _, l, predictions = session.run([optimizer, loss, train_prediction], feed_dict=feed_dict)
    if (step % 500 == 0):
      print("Minibatch loss at step %d: %f" % (step, l))
      print("Minibatch accuracy: %.1f%%" % accuracy(predictions, batch_labels))
      print("Validation accuracy: %.1f%%" % accuracy(valid_prediction.eval(), valid_labels))
  print("Test accuracy: %.1f%%" % accuracy(test_prediction.eval(), test_labels))






#######################################
### Problem 1
###   Introduce and tune L2 regularization
#######################################
# if isL2 :
#     loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(prediction(tf_train_dataset), tf_train_labels) )
# else :
#  loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(prediction(tf_train_dataset), tf_train_labels) + .05*tf.nn.l2_loss(weights))



#######################################
### Problem 2
###   Let's demonstrate an extreme case of overfitting
#######################################
# batch_size = 16


#######################################
### Problem 3
###   Introduce Dropout on the hidden 
###   layer of the neural network
#######################################
# def prediction(mInput, dropout=False):
#   layer1 = tf.nn.relu(tf.matmul(mInput, weights_h) + biases_h)
#   if dropout : layer1 = tf.nn.dropout(layer1, keep_prob)   # HERE WE ADD DROPOUT
#   logits = tf.matmul(layer1, weights) + biases
#   return logits


#######################################
### Problem 4
###   Try to get the best performance 
###   you can using a multi-layer model!
#######################################
### Only change the optimizer
# global_step = tf.Variable(0)  # count the number of steps taken.
# learning_rate = tf.train.exponential_decay(0.5, global_step, 100000, 0.96) # decay every 100000 steps with a base of 0.96
# optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)
# weights_h1 = tf.Variable(tf.truncated_normal([image_size * image_size, 1024]))


### OR introduce a 2nd layers
# weights_h1 = tf.Variable(tf.truncated_normal([image_size * image_size, 1024]))
# biases_h1  = tf.Variable(tf.zeros([1024]))
# weights_h2 = tf.Variable(tf.truncated_normal([1024, 1024]))
# biases_h2  = tf.Variable(tf.zeros([1024]))
# weights    = tf.Variable(tf.truncated_normal([1024, num_labels]))
# biases     = tf.Variable(tf.zeros([num_labels]))

# def prediction(mInput, dropout=False):
#   layer1 = tf.nn.relu(tf.matmul(mInput, weights_h1) + biases_h1)
#   if dropout : layer1 = tf.nn.dropout(layer1, keep_prob)
#   layer2 = tf.nn.relu(tf.matmul(layer1, weights_h2) + biases_h2)
#   logits = tf.matmul(layer2, weights) + biases
#   return logits

# optimizer = tf.train.AdamOptimizer(0.0005).minimize(cross_entropy)




