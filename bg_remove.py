import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import anthropic

# Function to convert image to base64
def get_image_base64(image):
    # Convert image to RGB if it has an alpha channel (RGBA)
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

# Initialize the Anthropic client
client = anthropic.Anthropic(api_key="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")

# User interface for uploading an image
st.write("## Upload your image for analysis")
uploaded_image = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_image:
    # Display the uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Convert the image to base64
    image_base64 = get_image_base64(image)

    # Create a message for the Anthropic API
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0,
        system="tell the user their season color based on the uploaded picture",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_base64
                        }
                    }
                ]
            }
        ]
    )

        # Display the response from the API
    st.write("**Analysis:**")
    # Access the text content directly from message.content (assuming it's a TextBlock)
    st.write(message.content)  # Assuming message.content is a TextBlock
