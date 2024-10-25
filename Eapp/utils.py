import requests

def upload_image_to_imgbb(image_file):
    url = "https://api.imgbb.com/1/upload"
    api_key = "2d57b31a66582a2c75234109512f3967"  # Your ImgBB API key

    # Prepare the payload with the API key and image file
    payload = {
        'key': api_key,
    }

    # Open the image file as binary and send the POST request
    files = {
        'image': image_file.read(),  # Read the binary content of the image
    }

    try:
        response = requests.post(url, data=payload, files=files)

        # Check if the upload was successful
        if response.status_code == 200:
            data = response.json()
            image_url = data['data']['url']  # The URL of the uploaded image on ImgBB
            return image_url
        else:
            print(f"Error uploading image: {response.text}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
