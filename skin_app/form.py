from django import forms

from tensorflow.keras.applications.resnet50 import preprocess_input
import cv2
from tensorflow.keras.models import load_model
import numpy as np

class SkinDiseasesClassificationForm(forms.Form):
    image = forms.ImageField()

    def predict(self):
        if self.is_valid():
            image_data = self.cleaned_data['image'].read()  # Read the image data
            image_path = self.cleaned_data['image']
            image_array = np.frombuffer(image_data, dtype=np.uint8)  # Convert to numpy array
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)  # Decode image
            img = cv2.resize(image, (224, 224))
            img = preprocess_input(np.array([img]))
            
            # Load the pre-trained model
            model = load_model('Skin_Diseases_AI\model\my_model.h5')
            classes = ['BA-cellulitis', 'BA-impetigo', 'FU-athlete-foot', 'FU-nail-fungus', 'FU-ringworm', 'PA-cutaneous-larva-migrans', 'VI-chickenpox', 'VI-shingles']
            
            # Predict
            pred = model.predict(img)
            predicted_class_index = np.argmax(pred)
            final_result = classes[predicted_class_index]
            accuracy = round(pred[0][predicted_class_index]*100,2)
            return final_result,accuracy