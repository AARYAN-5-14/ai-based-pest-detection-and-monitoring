import tensorflow as tf

# ------------------------------------
# PATHS (CHANGE IF NEEDED)
# ------------------------------------
TEST_DIR = r"classification\test"
MODEL_PATH = "pest_cnn_model.h5"

# ------------------------------------
# PARAMETERS
# ------------------------------------
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# ------------------------------------
# LOAD TEST DATASET
# ------------------------------------
test_ds = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    shuffle=False   # IMPORTANT for evaluation
)

# Normalize images
test_ds = test_ds.map(lambda x, y: (x / 255.0, y))

AUTOTUNE = tf.data.AUTOTUNE
test_ds = test_ds.prefetch(AUTOTUNE)

# ------------------------------------
# LOAD TRAINED MODEL
# ------------------------------------
model = tf.keras.models.load_model(MODEL_PATH)

print("✅ Model loaded successfully")

# ------------------------------------
# EVALUATE MODEL
# ------------------------------------
test_loss, test_accuracy = model.evaluate(test_ds)

print("\n📊 Test Results")
print("Test Loss     :", test_loss)
print("Test Accuracy :", test_accuracy)


