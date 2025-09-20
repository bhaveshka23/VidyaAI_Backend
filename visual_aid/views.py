import os
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import VisualAid
import google.generativeai as genai
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import json


genai.configure(api_key = settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


class Visual_aid(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    def post(self,request):
        try :
            question = request.data.get("question")
            image = request.FILES.get("image")

            if not question :
                return Response(
                    {'error' :'Question is required.'},
                    status = status.HTTP_400_BAD_REQUEST
                )

            #prompt for gemini

            prompt = f"""
                    You are a helpful assistant that converts teacher descriptions into clear, simple diagrams for classroom teaching.
                    - Output: Mermaid.js flowchart code (graph TD). Do not include explanations or extra text.
                    - Style: Minimal, blackboard-friendly, easy to read.
                    - Constraints: 
                      - Only include the elements mentioned in the description.
                      - Use short, clear node names.
                      - Show direction of process with arrows.
                      
                    Example Input: "Draw the water cycle with sun, evaporation, clouds, rain, and lake."
                    Example Output:
                        graph TD
                          Sun --> Evaporation
                          Evaporation --> Clouds
                          Clouds --> Rain
                          Rain --> Lake
                    
                    Now convert this description into a Mermaid.js flowchart:
                    
                    Description : "{question}"
            """

            inputs = [prompt]
            if image:
                inputs.append(
                    {
                        "mime_type": image.content_type,
                        "data": image.read()
                    }
                )

            # Call Gemini
            response = model.generate_content(inputs)
            mermaid_code = response.text.strip()

            if mermaid_code.startswith("```") and mermaid_code.endswith("```"):
                mermaid_code = mermaid_code.strip("`").split("\n", 1)[-1]

            # visual_aid = VisualAid.objects.create(
            #     user=request.user,
            #     question=question,
            #     mermaid_code=mermaid_code
            # )

            return Response({
                "question": question,
                "mermaid_code": mermaid_code
            }, status=status.HTTP_201_CREATED)


        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



