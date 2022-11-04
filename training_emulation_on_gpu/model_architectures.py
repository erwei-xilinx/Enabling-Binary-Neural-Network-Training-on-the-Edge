
import tensorflow as tf
import keras
from keras.models import Sequential, Model
from keras.layers import Dense, Convolution2D, Activation, Flatten, MaxPooling2D,Input,Dropout,GlobalAveragePooling2D
from keras.layers.normalization import BatchNormalization
from tensorflow.python.framework import ops
from binarization_utils import *

batch_norm_eps=1e-4
batch_norm_momentum=0.9

def get_model(dataset,resid_levels,batch_size, l1=1.0, l2=1.0, l3=1.0, l4=1.0, l5=1.0, l6=1.0, l7=1.0, l8=1.0):
	if dataset=='MNIST':
		model=Sequential()
		model.add(binary_dense(n_in=784,n_out=int(256*l1),input_shape=[784],first_layer=True))
		model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		# model.add(l1_batch_norm_mod_dense(batch_size=batch_size,ch_in=256*l1,momentum=batch_norm_momentum))
		model.add(binary_activation())
		model.add(binary_dense(n_in=int(model.output.get_shape()[1]),n_out=int(256*l2)))
		model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		# model.add(l1_batch_norm_mod_dense(batch_size=batch_size,ch_in=256*l2,momentum=batch_norm_momentum))
		model.add(binary_activation())
		model.add(binary_dense(n_in=int(model.output.get_shape()[1]),n_out=int(256*l3)))
		model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		# model.add(l1_batch_norm_mod_dense(batch_size=batch_size,ch_in=256*l3,momentum=batch_norm_momentum))
		model.add(binary_activation())
		model.add(binary_dense(n_in=int(model.output.get_shape()[1]),n_out=int(256*l4)))
		model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		# model.add(l1_batch_norm_mod_dense(batch_size=batch_size,ch_in=256*l4,momentum=batch_norm_momentum))
		model.add(binary_activation())
		model.add(binary_dense(n_in=int(model.output.get_shape()[1]),n_out=10))
		model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		# model.add(l1_batch_norm_mod_dense(batch_size=batch_size,ch_in=10,momentum=batch_norm_momentum))
		model.add(Activation('softmax'))

	elif dataset=="CIFAR-10" or dataset=="SVHN":
		model=Sequential()
		model.add(binary_conv(nfilters=64,ch_in=3,k=3,padding='valid',input_shape=[32,32,3],first_layer=True))
		#model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		model.add(l1_batch_norm_mod_conv(batch_size=batch_size,width_in=30,ch_in=64,momentum=batch_norm_momentum))
		model.add(binary_activation())
		model.add(binary_conv(nfilters=64,ch_in=64,k=3,padding='valid'))
		#model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		model.add(l1_batch_norm_mod_conv(batch_size=batch_size,width_in=28,ch_in=64,momentum=batch_norm_momentum))
		model.add(binary_activation())
		model.add(MaxPooling2D(pool_size=(2, 2),strides=(2,2)))

		model.add(binary_conv(nfilters=128,ch_in=64,k=3,padding='valid'))
		#model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		model.add(l1_batch_norm_mod_conv(batch_size=batch_size,width_in=12,ch_in=128,momentum=batch_norm_momentum))
		model.add(binary_activation())
		model.add(binary_conv(nfilters=128,ch_in=128,k=3,padding='valid'))
		#model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		model.add(l1_batch_norm_mod_conv(batch_size=batch_size,width_in=10,ch_in=128,momentum=batch_norm_momentum))
		model.add(binary_activation())
		model.add(MaxPooling2D(pool_size=(2, 2),strides=(2,2)))

		model.add(binary_conv(nfilters=256,ch_in=128,k=3,padding='valid'))
		#model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		model.add(l1_batch_norm_mod_conv(batch_size=batch_size,width_in=3,ch_in=256,momentum=batch_norm_momentum))
		model.add(binary_activation())
		model.add(binary_conv(nfilters=256,ch_in=256,k=3,padding='valid'))
		#model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		model.add(l1_batch_norm_mod_conv(batch_size=batch_size,width_in=1,ch_in=256,momentum=batch_norm_momentum))
		model.add(binary_activation())

		model.add(my_flat())

		model.add(binary_dense(n_in=int(model.output.get_shape()[1]),n_out=512))
		#model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		model.add(l1_batch_norm_mod_dense(batch_size=batch_size,ch_in=512,momentum=batch_norm_momentum))
		model.add(binary_activation())
		model.add(binary_dense(n_in=int(model.output.get_shape()[1]),n_out=512))
		#model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		model.add(l1_batch_norm_mod_dense(batch_size=batch_size,ch_in=512,momentum=batch_norm_momentum))
		model.add(binary_activation())
		model.add(binary_dense(n_in=int(model.output.get_shape()[1]),n_out=10))
		#model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		model.add(l1_batch_norm_mod_dense(batch_size=batch_size,ch_in=10,momentum=batch_norm_momentum))
		model.add(Activation('softmax'))

	elif dataset=="binarynet" or dataset=="binarynet-svhn":
		model=Sequential()
		model.add(binary_conv(nfilters=int(128*l1),ch_in=3,k=3,padding='same',input_shape=[32,32,3],first_layer=True))
		model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		# model.add(l1_batch_norm_mod_conv(batch_size=batch_size,width_in=32,ch_in=128,momentum=batch_norm_momentum))
		model.add(binary_activation())
		model.add(binary_conv(nfilters=int(128*l2),ch_in=int(128*l1),k=3,padding='same'))
		model.add(MaxPooling2D(pool_size=(2, 2),strides=(2,2)))
		model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		# model.add(l1_batch_norm_mod_conv(batch_size=batch_size,width_in=16,ch_in=128,momentum=batch_norm_momentum))
		model.add(binary_activation())

		model.add(binary_conv(nfilters=int(256*l3),ch_in=int(128*l2),k=3,padding='same'))
		model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		# model.add(l1_batch_norm_mod_conv(batch_size=batch_size,width_in=16,ch_in=256,momentum=batch_norm_momentum))
		model.add(binary_activation())
		model.add(binary_conv(nfilters=int(256*l4),ch_in=int(256*l3),k=3,padding='same'))
		model.add(MaxPooling2D(pool_size=(2, 2),strides=(2,2)))
		model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		# model.add(l1_batch_norm_mod_conv(batch_size=batch_size,width_in=8,ch_in=256,momentum=batch_norm_momentum))
		model.add(binary_activation())

		model.add(binary_conv(nfilters=int(512*l5),ch_in=int(256*l4),k=3,padding='same'))
		model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		# model.add(l1_batch_norm_mod_conv(batch_size=batch_size,width_in=8,ch_in=512,momentum=batch_norm_momentum))
		model.add(binary_activation())
		model.add(binary_conv(nfilters=int(512*l6),ch_in=int(512*l5),k=3,padding='same'))
		model.add(MaxPooling2D(pool_size=(2, 2),strides=(2,2)))
		model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		# model.add(l1_batch_norm_mod_conv(batch_size=batch_size,width_in=4,ch_in=512,momentum=batch_norm_momentum))
		model.add(binary_activation())

		model.add(my_flat())

		model.add(binary_dense(n_in=int(model.output.get_shape()[1]),n_out=int(1024*l7)))
		model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		# model.add(l1_batch_norm_mod_dense(batch_size=batch_size,ch_in=1024,momentum=batch_norm_momentum))
		model.add(binary_activation())
		model.add(binary_dense(n_in=int(model.output.get_shape()[1]),n_out=int(1024*l8)))
		model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		# model.add(l1_batch_norm_mod_dense(batch_size=batch_size,ch_in=1024,momentum=batch_norm_momentum))
		model.add(binary_activation())
		model.add(binary_dense(n_in=int(model.output.get_shape()[1]),n_out=10))
		model.add(BatchNormalization(axis=-1, momentum=batch_norm_momentum, epsilon=batch_norm_eps))
		# model.add(l1_batch_norm_mod_dense(batch_size=batch_size,ch_in=10,momentum=batch_norm_momentum))
		model.add(Activation('softmax'))
	else:
		raise("dataset should be one of the following list: [MNIST, CIFAR-10, SVHN, binarynet].")
	return model
