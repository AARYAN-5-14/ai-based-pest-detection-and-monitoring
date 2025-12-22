import tensorflow as tf
from tensorflow.keras import layers, models

# --------------------------------------------------
# DATASET PATHS (CHANGE ONLY IF YOUR PATH IS DIFFERENT)
# --------------------------------------------------
TRAIN_DIR = r"classification\train"
VAL_DIR   = r"classification\val"

# --------------------------------------------------
# PARAMETERS
# --------------------------------------------------
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
NUM_CLASSES = 102   # total pest classes
EPOCHS = 10         # increase later if needed

# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------
train_ds = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int"
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    VAL_DIR,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int"
)

# --------------------------------------------------
# NORMALIZE IMAGES
# --------------------------------------------------
train_ds = train_ds.map(lambda x, y: (x / 255.0, y))
val_ds   = val_ds.map(lambda x, y: (x / 255.0, y))

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(AUTOTUNE)
val_ds   = val_ds.prefetch(AUTOTUNE)

# --------------------------------------------------
# DATA AUGMENTATION
# --------------------------------------------------
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

# --------------------------------------------------
# CNN MODEL (FIXED VERSION)
# --------------------------------------------------
model = models.Sequential([
    layers.Input(shape=(224, 224, 3)),   # IMPORTANT FIX

    data_augmentation,

    layers.Conv2D(32, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(128, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(NUM_CLASSES, activation='softmax')
])

# --------------------------------------------------
# COMPILE MODEL
# --------------------------------------------------
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# --------------------------------------------------
# MODEL SUMMARY
# --------------------------------------------------
model.summary()

# --------------------------------------------------
# TRAIN MODEL
# --------------------------------------------------
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS
)

# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------
model.save("pest_cnn_model.h5")

print("✅ CNN model trained and saved as pest_cnn_model.h5")
