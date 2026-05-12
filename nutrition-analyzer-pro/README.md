# AI Nutrition Analyzer (Pro Version)
This is a Python desktop application that uses Google's Gemini AI to perform a detailed nutritional analysis of a food item from an uploaded image.

## 🧠 AI Pipeline Architecture

```
User Uploads Image<br>
        ↓<br>
Tkinter Desktop App
        ↓<br>
Gemini AI Vision Model<br>
        ↓<br>
Nutrition Report Generated<br>
        ↓<br>
Displayed to User & Logged Locally<br>
```

## Features
-   **Image-Based Analysis:** Simply upload a photo of your meal to get started.
-   **Detailed Reporting:** Receives a full breakdown including calories, macronutrients, micronutrients, and health insights.
-   **Personal Logging:** Automatically saves every analysis to a local `nutrition_log_pro.csv` file for personal tracking (this file is excluded from the repository).
-   **Simple Desktop GUI:** Built with Python's native Tkinter library for a straightforward user experience.

## Setup and Installation
Follow these steps to get the application running on your local machine.

#### **1. Clone the Repository**
First, clone this repository to your computer: git clone https://github.com/Kamalesh-Suresh-Kumar/VI-Foundations-of-Artificial-Intelligence.git
Second, Navigate into the project directory: cd nutrition-analyzer-pro

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


#### **4. Obtaining Your Gemini API Key
To use this application, you need a free API key from Google AI Studio. This key acts as a password that allows your code to access the Gemini models. Follow these steps to get yours.

# Step 1: Go to Google AI Studio
Navigate to the official Google AI Studio website[https://aistudio.google.com/]. You will need to sign in with your Google Account.

# Step 2: Create a New API Key
1. Once you are in Google AI Studio, look for the "Get API key" button, usually located on the left-hand menu or near the top.
2. Click on it. A new screen will appear. Click the button that says "Create API key in new project".
3. Google will generate a new project and a unique API key for you.

# Step 3: Copy Your API Key
1. A pop-up window will display your newly generated API key. This is a long string of letters and numbers.
2. Click the copy icon next to the key to copy it to your clipboard.

#### ***Important: Treat this key like a password. Do not share it publicly or commit it to version control systems like GitHub.

#### **5. Set Up Your API Key
1. Create a file named .env in the main project folder.
2. Inside this file, add your Google Gemini API key like this:
GEMINI_API_KEY="YOUR_API_KEY_HERE"

#### **6. How to Run the Application
With your environment activated and the dependencies installed, run the following command in your terminal:

# Activate the environment
venv\Scripts\activate

# Run Application
python app.py


#### **7. Project Structure

nutrition-analyzer/<br>
│<br>
├── test_imgs/          <- Optional: Contains some images for testing. Also Ignored by Git<br>
├── .env                <- Ignored by Git<br>
├── venv/               <- Ignored by Git<br>
├── nutrition_log_pro.csv   <- Ignored by Git<br>
│<br>
├── .gitignore<br>
├── README.md<br>
│<br>
├── app.py<br>
├── test_key.py<br>
└── requirements.txt<br>

## Summary
This project is a desktop application built with Python and Tkinter that leverages **Google's Gemini AI** to provide a detailed nutritional analysis from a single image of food.

A user can upload a photo of their meal, input an estimated portion size, and the application utilizes the powerful `gemini-2.5-pro` vision model to identify the food and generate a comprehensive report. The report includes estimated calories, macronutrients (protein, carbohydrates, fat), key micronutrients, and general health insights. For personal tracking, each analysis is automatically saved to a local `nutrition_log_pro.csv` file.

### Author:
Kamalesh S P<br>
230701138<br>
REC