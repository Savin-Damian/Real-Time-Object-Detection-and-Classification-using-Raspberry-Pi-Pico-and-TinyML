import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt


data = pd.read_csv('distance.csv') 


labels = {'COLIZIUNE': 0, 'ALERT': 1, 'OK': 2}
data['label'] = data['Mesaj'].map(labels)  


X = data[['Distanta_cm']].values  # Folosim doar coloana Distanta_cm
scaler = StandardScaler()
X = scaler.fit_transform(X)  

y = data['label'].values  # Etichetele pentru mesaje (0: COLIZIUNE, 1: ALERT, 2: OK)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation='relu', input_shape=(X_train.shape[1],)),  # Strat ascuns
    tf.keras.layers.Dropout(0.5),  # Regularizare pentru a preveni overfitting-ul
    tf.keras.layers.Dense(64, activation='relu'),  # Alt strat ascuns
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(3, activation='softmax')  
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),  # Optimizator
              loss='sparse_categorical_crossentropy',  
              metrics=['accuracy'])


early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)

history = model.fit(X_train, y_train, epochs=100, validation_data=(X_test, y_test), callbacks=[early_stop])


model.save('distance_classifier_v2.h5')
print("Modelul a fost salvat cu succes!")


test_loss, test_accuracy = model.evaluate(X_test, y_test)  
print(f'Loss: {test_loss:.4f}, Accuracy: {test_accuracy:.4f}')

# Prezicerea pe datele de test
y_pred = model.predict(X_test)
y_pred_classes = y_pred.argmax(axis=-1)  

print(classification_report(y_test, y_pred_classes))
conf_matrix = confusion_matrix(y_test, y_pred_classes)

# Vizualizarea matricei de confuzie
plt.figure(figsize=(6,6))
plt.imshow(conf_matrix, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.colorbar()
classes = ['COLIZIUNE', 'ALERT', 'OK']
tick_marks = range(len(classes))
plt.xticks(tick_marks, classes)
plt.yticks(tick_marks, classes)
plt.xlabel('Predicted label')
plt.ylabel('True label')
plt.show()
