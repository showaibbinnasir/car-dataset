from PIL import Image
import requests
from io import BytesIO

response = requests.get("https://i.ibb.co/NCBNFKD/logo.png")
img = Image.open(BytesIO(response.content))

