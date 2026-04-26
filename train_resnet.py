import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
import matplotlib.pyplot as plt

# ---------------- SETTINGS ---------------- #
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 30

# ---------------- DATA ---------------- #
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=30,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2]
)

train = datagen.flow_from_directory(
    'dataset/train',
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

val = datagen.flow_from_directory(
    'dataset/train',
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False   # 🔥 important for evaluation
)

# ---------------- CLASS WEIGHTS ---------------- #
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(train.classes),
    y=train.classes
)
class_weights = dict(enumerate(class_weights))

# ---------------- RESNET MODEL ---------------- #
base_model = ResNet50(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)

# 🔥 Partial Fine-Tuning
for layer in base_model.layers[:-30]:
    layer.trainable = False

for layer in base_model.layers[-30:]:
    layer.trainable = True

# ---------------- CUSTOM HEAD ---------------- #
x = base_model.output
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.BatchNormalization()(x)
x = tf.keras.layers.Dense(256, activation='relu')(x)
x = tf.keras.layers.Dropout(0.5)(x)
output = tf.keras.layers.Dense(train.num_classes, activation='softmax')(x)

model = tf.keras.Model(inputs=base_model.input, outputs=output)

# ---------------- COMPILE ---------------- #
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# ---------------- CALLBACKS ---------------- #
early_stop = EarlyStopping(patience=5, restore_best_weights=True)

reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.3,
    patience=3,
    min_lr=1e-6
)

# ---------------- TRAIN ---------------- #
history = model.fit(
    train,
    validation_data=val,
    epochs=EPOCHS,
    class_weight=class_weights,
    callbacks=[early_stop, reduce_lr]
)

# ---------------- SAVE ---------------- #
model.save("model/resnet_model.h5")

# ---------------- EVALUATION ---------------- #
y_true = val.classes
y_pred = model.predict(val)
y_pred_classes = np.argmax(y_pred, axis=1)

print("\n📊 Classification Report:")
print(classification_report(y_true, y_pred_classes))

# AUC
try:
    auc = roc_auc_score(tf.keras.utils.to_categorical(y_true), y_pred)
    print("✅ AUC Score:", auc)
except:
    print("⚠️ AUC not supported")

# ---------------- GRAPH ---------------- #
plt.figure()
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('ResNet Accuracy')
plt.legend(['Train', 'Validation'])
plt.show()

# ---------------- SUMMARY ---------------- #
model.summary()