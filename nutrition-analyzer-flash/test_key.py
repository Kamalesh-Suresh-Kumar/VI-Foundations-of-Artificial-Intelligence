import os
import google.generativeai as genai
from dotenv import load_dotenv

def check_api_key():
    """
    A simple function to test if the Gemini API key is working.
    """
    try:
        # Load the environment variables from the .env file
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            print("Error: GEMINI_API_KEY not found in .env file.")
            return

        # Configure the generative AI library
        genai.configure(api_key=api_key)

        # Create a model and send a simple prompt
        print("... Contacting Google Gemini AI ...")
        model = genai.GenerativeModel('gemini-2.5-pro') # Update to the latest model if needed
        response = model.generate_content("Test prompt: Please respond with 'Hello!' if this works.")
        
        # Check the response
        print(f"AI Response: {response.text}")
        print("\nSuccess! Your API key is configured correctly and is working.")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("\nYour API key might be invalid or there could be a connection issue.")

# Run the check
if __name__ == "__main__":
    check_api_key()