from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import numpy as np 
from keras.preprocessing import image
import os

img_width,img_height=150,150

train_data_dir='C:/Users/rithik/Desktop/PetImages'
validation_data_dir='C:/Users/rithik/Desktop/PetImages'
nb_train_samples=1000
nb_validation_samples=100
epochs=5
batch_size=20

if K.image_data_format()=='channels_first':
	input_shape(3,img_width,img_height)
else:
	input_shape=(img_width,img_height,3)

train_datagen=ImageDataGenerator(rescale=1. /255,
	shear_range=0.2,
	zoom_range=0.2,
	horizontal_flip=True)

test_datagen=ImageDataGenerator(rescale=1./255)		

train_generator=train_datagen.flow_from_directory(
	train_data_dir,
	target_size=(img_width,img_height),
	batch_size=batch_size,
	class_mode='binary')

validation_generator=test_datagen.flow_from_directory(
	validation_data_dir,
	target_size=(img_width,img_height),
	batch_size=batch_size,
	class_mode='binary')


model= Sequential()
model.add(Conv2D(32,(3,3),input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.summary()

model.add(Conv2D(32,(3,3),input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(64,(3,3),input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.summary()

model.compile(
	loss='binary_crossentropy',
	optimizer='rmsprop',
	metrics=['accuracy'])


model.fit_generator(
	train_generator,
	steps_per_epoch=nb_train_samples // batch_size,
	epochs=epochs,
	validation_data=validation_generator,
	validation_steps=nb_train_samples //batch_size)


save_model(model, 'my_model.h5') # model, [path + "/"] name of model

# Deletes the existing model
#del model  

# Returns a compiled model identical to the previous one
#new_model = load_model('my_model.h5')

img_pred=image.load_img('/Desktop/PetImages/Dog/1.jpg',target_size=(150,150))
img_pred=image.img_to_array(img_pred)
img_pred=np.expand_dims(img_pred, axis=0)

rslt=model.predict(img_pred)
print(rslt)
if rslt[0][0]==1:
	prediction="Dog"
else:
	prediction="Cat"

print(prediction)		