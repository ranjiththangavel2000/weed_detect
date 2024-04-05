from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from PIL import Image, UnidentifiedImageError
import io
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2
app = FastAPI()

# Define allowed origins
origins = [
    "http://localhost:3000",
    # Add other origins as needed
]

# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model
model = load_model("efficientnet_model.h5")

# Redefine class labels dictionary
class_labels = {0: 'class1', 1: 'class2', 2: 'class3', 3: 'class4'}

# Function to classify image and return result
def classify_image(image_bytes):
    try:
        # Attempt to open using Pillow (for potential JPEG/PNG)
        image = Image.open(io.BytesIO(image_bytes))
    except UnidentifiedImageError:
        # If Pillow fails, assume TIFF and use OpenCV
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    # Convert the image to a NumPy array
    image_np = np.array(image)

    # Resize the image to match the model's input size
    resized_image = cv2.resize(image_np, (224, 224))

    # Convert the image to float32 (required by EfficientNet)
    input_image = resized_image.astype(np.float32)

    # Apply preprocessing as required by the EfficientNet model
    input_image = preprocess_input(input_image)

    # Expand dimensions to create batch dimension
    input_image = np.expand_dims(input_image, axis=0)

    # Make predictions
    predictions = model.predict(input_image)

    # Interpret predictions
    predicted_class = np.argmax(predictions)
    predicted_label = class_labels[predicted_class]
    print(predicted_label)

    return predicted_label


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    image=Image.open(io.BytesIO(contents))
    image.show()

    # Check file extension (optional, informative)
    filename = file.filename

    if not filename.lower().endswith(".tif"):
        raise HTTPException(status_code=415, detail="Unsupported image format. Please upload a TIFF image.")

    predicted_label = classify_image(contents)

    # Check the predicted class and return appropriate response
    if predicted_label == 'class1' or predicted_label == 'class2' :
        return {"result": "weed detected"}
    elif predicted_label == 'class3' or predicted_label == 'class4':
        return {"result": "weed not detected"}
    else:
        raise HTTPException(status_code=500, detail="Error in prediction")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)