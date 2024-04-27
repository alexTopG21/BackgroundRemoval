import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import base64

def get_image_base64(image):
    # Convert image to base64 for API submission
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

# User interaction for uploading an image
st.write("## Upload your image for analysis")
uploaded_image = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_image:
    # Display the uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Convert image to base64
    image_base64 = get_image_base64(image)
    image_media_type = "image/jpeg"  # Adjust as necessary based on the image format
    
    # API request setup
    api_key = "your_api_key_here"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image_media_type,
                            "data": image_base64,
                        },
                    },
                    {
                        "type": "text",
                        "text": "Describe this image."
                    }
                ],
            }
        ]
    }
    
    # API URL
    api_url = "https://api.anthropic.com/your_model_endpoint"
    
    # Send the request
    response = requests.post(api_url, json=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        st.write("## Analysis by Claude")
        st.write(result["description"])  # Modify according to the actual key in the response
    else:
        st.error("Failed to analyze the image. Please try again.")

# Sidebar with additional resources
st.sidebar.write("## Additional Resources")
st.sidebar.write("Learn more about how colors can enhance your style and appearance.")
