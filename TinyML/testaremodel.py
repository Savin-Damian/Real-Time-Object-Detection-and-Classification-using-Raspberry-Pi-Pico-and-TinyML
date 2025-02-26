
import tensorflow as tf

model = tf.keras.models.load_model('D:/Date hard/Facultate AC/An 4/Sem1/SI/Proiect/TinyML/distance_classifier_v2.h5')

# Conversia la model TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open('distance_classifier.tflite', 'wb') as f:
    f.write(tflite_model)
