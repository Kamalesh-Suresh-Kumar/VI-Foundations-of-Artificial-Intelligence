import os
import google.generativeai as genai
from dotenv import load_dotenv
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

# Import config variables
from config import (
    CLARIFAI_USER_ID, CLARIFAI_APP_ID, CLARIFAI_MODEL_ID, 
    GEMINI_MODEL_NAME, MIN_CONFIDENCE
)

# --- 1. CLARIFAI API SETUP & FUNCTION ---

# Load the Clarifai Personal Access Token (PAT)
load_dotenv()
CLARIFAI_PAT = os.getenv("CLARIFAI_PAT")
if not CLARIFAI_PAT:
    raise ValueError("CLARIFAI_PAT not found in .env file.")

# Set up the gRPC channel (this is the standard way to connect to Clarifai)
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)
metadata = (("authorization", f"Key {CLARIFAI_PAT}"),)

def identify_food_from_image(image_path):
    """
    Identifies food from an image using the Clarifai API.
    Returns the name of the top-confidence food item.
    Raises an error if no food is identified with sufficient confidence.
    """
    with open(image_path, "rb") as f:
        file_bytes = f.read()

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=resources_pb2.UserAppIDSet(user_id=CLARIFAI_USER_ID, app_id=CLARIFAI_APP_ID),
            model_id=CLARIFAI_MODEL_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(image=resources_pb2.Image(base64=file_bytes))
                )
            ],
        ),
        metadata=metadata,
    )

    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        raise Exception(f"Clarifai API error: {post_model_outputs_response.status.description}")

    if not post_model_outputs_response.outputs[0].data.concepts:
        raise ValueError("No food items were identified in the image.")

    # Get the top prediction
    top_concept = post_model_outputs_response.outputs[0].data.concepts[0]
    food_name = top_concept.name
    confidence = top_concept.value

    print(f"Clarifai identified: {food_name} (Confidence: {confidence:.2%})")

    # Check if the confidence is high enough
    if confidence < MIN_CONFIDENCE:
        raise ValueError(f"Food identification confidence ({confidence:.2%}) is below the {MIN_CONFIDENCE:.0%} threshold. Please use a clearer image.")

    return food_name

# --- 2. GEMINI API SETUP & FUNCTION ---

# Load the Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

genai.configure(api_key=GEMINI_API_KEY)

def generate_report_from_name(food_name, quantity_string):
    """
    Generates a nutritional report from a food name using the Gemini API.
    """
    model = genai.GenerativeModel(GEMINI_MODEL_NAME)
    
    prompt = f"""
    You are an expert nutritionist. Generate a detailed nutritional analysis for the food item "{food_name}" with an estimated portion size of "{quantity_string}".

    Your response MUST be in this exact markdown format, filling in the bracketed information:

    **1. Food Identification:**
    * **Primary food item:** {food_name.title()}
    * **Estimated portion size:** {quantity_string}

    **2. Estimated Nutritional Information (per serving):**
    * **Calories:** [Number] kcal
    * **Macronutrients:**
        * Protein: [Number]g
        * Carbohydrates: [Number]g
        * Fat: [Number]g
    * **Micronutrients:**
        * Sugar: [Number]g
        * Sodium: [Number]mg
        * Fiber: [Number]g

    **3. Health Insights:**
    * **Summary:** [A brief summary of health benefits or considerations.]
    * **Potential Allergens:** [List any potential common allergens.]
    """
    
    response = model.generate_content(prompt)
    return response.text