# AI Nutrition Analyzer (Flash Version)
This is a Python desktop application that uses Google's Gemini AI and the Clarifai API to perform a detailed nutritional analysis of a food item from an uploaded image.

## 🧠 AI Pipeline Architecture

```
User Uploads Image
        ↓
Tkinter Desktop App
        ↓
Clarifai Food Detection API
        ↓
Food Name Extracted
        ↓
Gemini AI Analysis
        ↓
Nutrition Report Generated
        ↓
Displayed to User & Logged Locally
```

## API Details
This project seamlessly links two advanced AI APIs to generate its reports:

1. **Food Recognition via Clarifai API ([clarifai.com](https://clarifai.com/))**:
   * The uploaded food image is securely sent to Clarifai's computer vision gRPC server using the `food-item-recognition` model.
   * Clarifai analyzes the image and returns the most probable food name with high confidence.
2. **Report Generation via Google Gemini API([Gemini AI Studio](https://aistudio.google.com/))**:
   * The food name identified by Clarifai, along with the portion size you specify, is sent to Google's Gemini AI (`gemini-2.5-flash`).
   * Gemini acts as a professional nutritionist and generates a structured markdown report including calories, macronutrients (Protein, Carbs, Fat), micronutrients, and potential health insights/allergens.

## Features
-   **Image-Based Analysis:** Simply upload a photo of your meal to get started.
-   **Dual-AI Integration:** Combines Computer Vision (Clarifai) and Generative Text (Gemini) into one smooth pipeline.
-   **Detailed Reporting:** Receives a full breakdown including calories, macronutrients, micronutrients, and health insights.
-   **Personal Logging:** Automatically logs all your analyses to a local `nutrition_log_flash.csv` file for personal tracking (this file is excluded from the repository).
-   **Background Processing:** API calls are handled in background threads to ensure the UI remains responsive.
-   **Simple Desktop GUI:** Built with Python's native Tkinter library for a straightforward user experience.

## Setup and Installation
Follow these steps to get the application running on your local machine.

#### **1. Clone the Repository**
First, clone this repository to your computer: git clone https://github.com/Kamalesh-Suresh-Kumar/VI-Foundations-of-Artificial-Intelligence.git
Second, Navigate into the project directory: cd nutrition-analyzer-flash

#### **2. Create and Activate a Virtual Environment**
set up a Python virtual environment.

# Create the environment
python -m venv venv
# Activate on Windows
venv\Scripts\activate
# Activate on macOS/Linux
source venv/bin/activate


#### **3. Install Dependencies
To run this project, use the command below to install all the necessary libraries from the requirements file.

# Install all the necessary libraries
pip install -r requirements.txt


#### **4. Obtaining Your API Keys
To use this application, you need active API keys for both Clarifai and Google Gemini.
- **Clarifai:** Sign up at clarifai.com and generate a Personal Access Token (PAT).
- **Google Gemini:** Go to Google AI Studio and create a new API key.
*(Important: Treat these keys like passwords. Do not share them publicly or commit them to version control systems like GitHub.)*


#### **5. Set Up Your API Keys
1. Create a file named .env in the main project folder.
2. Inside this file, add your API keys like this:
CLARIFAI_PAT="YOUR_CLARIFAI_PAT_HERE"
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"


#### **6. How to Run the Application
With your environment activated and the dependencies installed, run the following command in your terminal:

# Activate the environment
venv\Scripts\activate

# Run Application
python app.py


#### **7. Project Structure

nutrition-analyzer-flash/<br>
│<br>
├── test_imgs/          <- Optional: Contains some images for testing. Also Ignored by Git<br>
├── .env                <- Ignored by Git<br>
├── venv/               <- Ignored by Git<br>
├── nutrition_log_flash.csv   <- Ignored by Git<br>
│<br>
├── .gitignore<br>
├── README.md<br>
│<br>
├── app.py<br>
├── ai_pipelines.py<br>
├── config.py<br>
├── test_key.py<br>
└── requirements.txt<br>


## Summary
This project is a desktop application built with Python and Tkinter that leverages **Clarifai's Computer Vision API** and **Google's Gemini AI** to provide a detailed nutritional analysis from a single image of food.

A user can upload a photo of their meal and input an estimated portion size. The application first sends the image to Clarifai to identify the food. Then, it utilizes the `gemini-2.5-flash` model to act as a professional nutritionist, generating a comprehensive report based on the identified food and portion. The report includes estimated calories, macronutrients (protein, carbohydrates, fat), key micronutrients, and general health insights. For personal tracking, each analysis is automatically saved to a local `nutrition_log_flash.csv` file.

### Author:
Kamalesh S P<br>
230701138<br>
REC