import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

genai.configure(api_key = settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_text_from_image(image_file):
    """
    Extract text from uploaded image using Tesseract OCR.
    :param image_file: Django InMemoryUploadedFile
    :return: extracted text as string
    """
    # Reset file pointer
    image_file.seek(0)

    # Open with PIL
    image = Image.open(image_file)
    image = image.convert("RGB")  # ensure compatible format

    # Run OCR
    text = pytesseract.image_to_string(image, lang='eng')  # change lang if needed
    return text.strip()


def build_worksheet_prompt(diff ,type, total_marks, lang , textbook_text):
    prompt = f"""
        You are an expert educator and worksheet generator.
        The user will provide a source content and  generate **three separate worksheets** in {lang} language.
        
        📌 Requirements:
            -Source Content:{textbook_text}
            - Difficulty: {diff}
            - Total Marks: {total_marks}
            - Only use the **{type}** question format (do not mix with others)
            - Provide clear instructions
            - Marking scheme so total = {total_marks}
            - Answer key at the end
            
            Output format:
            1. Title of the worksheet
            2. Instructions for students
            3. Questions with marks (all in {type} format)
            4. Answer key
            """
    return prompt


class Worksheet_generator(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self,request):
        try:
            image  = request.FILES.get("image")
            type = request.data.get("type")
            total_marks = request.data.get("total_marks")
            lang = request.data.get("lang")

            if not all ([image,type,total_marks,lang]):
                return Response({'error':'required all the feilds'} , status = status.HTTP_400_BAD_REQUEST)

            textbook_text = extract_text_from_image(image)

            difficulties = ['easy' , 'medium' , 'hard']
            worksheets = {}

            for diff in difficulties:
                prompt = build_worksheet_prompt(diff,type,total_marks,lang,textbook_text)
                response = model.generate_content([prompt])
                worksheets[diff] = response.text



            return Response({'worksheets':worksheets}, status = status.HTTP_201_CREATED)


        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






