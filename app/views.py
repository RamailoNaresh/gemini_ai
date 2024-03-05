import json
from django.shortcuts import render
import google.generativeai as genai
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from PIL import Image
from .serializers import ImageSerializers
from .models import ImageModel
import os
from dotenv import load_dotenv
load_dotenv()


GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")
def generate_respones(question):
    response = model.generate_content(question)
    return response


@api_view(["POST"])
def home(request):
    question = request.data["question"]
    response_data = generate_respones(question)
    formatted_response = f'''
    **Response:**
    {response_data.text}
    '''

    return Response({"message": formatted_response})



another_model = genai.GenerativeModel("gemini-pro-vision")


def generate_image_response(image):
    try:
        response = another_model.generate_content(image)
        return response.text
    except Exception as e:
        return str(e)


@api_view(["POST"])
def image_response(request):
    data = JSONParser().parse(request)
    image = data["image"]
    if image is not None:
        image_data = Image.open(image)
        response = generate_image_response(image_data)
        return Response({"message": response})
    return Response({"error": "Error occurred"})