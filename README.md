# Nutritionist Generative AI Doctor Using Gemini

Welcome to the **Foundations of Artificial Intelligence (FOAI)** project repository. This folder contains the complete project workspace, including documentation, architectural diagrams, and two distinct Python desktop applications designed to perform detailed nutritional analysis of food items from uploaded images.

## 📁 Repository Structure Overview

This repository is logically divided into project documentation, system diagrams, and two separate implementation codebases:

### 1. Documentation & Presentations
- **`NUTRITIONIST GENERATIVE AI DOCTOR USING GEMINI.docx` & `.pdf`**: The comprehensive final project report detailing the literature review, proposed system, architecture, and evaluation.
- **`CS23533 – FOAI Review -- PPT.pptx` & `.pdf`**: Presentation slides created for the academic project review, outlining the objectives, methodology, and outcomes of the AI Nutrition Analyzer.

### 2. Architectural Diagrams
- **`foai.drawio.png` & `foai ot.png`**: Visual representations of the project's data flow and architecture, illustrating how user inputs are processed by different AI models to produce the final nutritional report.

### 3. Code Implementations
The project features two distinct approaches to solving the core problem, housed in separate subdirectories:
- **[`nutrition-analyzer-flash/`](./nutrition-analyzer-flash/)**: A hybrid pipeline using the Clarifai API for image recognition and Gemini 2.5 Flash for report generation.
- **[`nutrition-analyzer-pro/`](./nutrition-analyzer-pro/)**: A streamlined pipeline using the Gemini 2.5 Pro multimodal vision model directly for both image recognition and report generation.

---

## 🔍 Sub-Project Details & Comparison

### A. Nutrition Analyzer (Flash Version)
*Located in `nutrition-analyzer-flash/`*

This version leverages a **Dual-AI Pipeline** integrating dedicated Computer Vision with Generative AI.
*   **Architecture**:
    1.  **Frontend**: Desktop Application built with Python `Tkinter`.
    2.  **Clarifai API**: The image is sent to Clarifai's `food-item-recognition` model to accurately identify the food item.
    3.  **Google Gemini AI**: The identified food name and user-defined portion size are sent to the `gemini-2.5-flash` model. Gemini acts as the nutritionist, structuring the data and generating a comprehensive markdown report.
*   **Logging**: Automatically logs all interactions and reports to a local `nutrition_log_flash.csv` file.
*   **Strengths**: Fast text generation by utilizing a specialized computer vision model as a preliminary step.

### B. Nutrition Analyzer (Pro Version)
*Located in `nutrition-analyzer-pro/`*

This version utilizes a **Unified Multimodal AI Pipeline**, relying entirely on Google's advanced Gemini vision capabilities.
*   **Architecture**:
    1.  **Frontend**: Desktop Application built with Python `Tkinter`.
    2.  **Gemini AI Vision Model**: The image and portion size are sent directly to the `gemini-2.5-pro` model. The model analyzes the image directly, identifies the food contextually, and generates the detailed nutritional report in a single API call.
*   **Logging**: Automatically logs all interactions and reports to a local `nutrition_log_pro.csv` file.
*   **Strengths**: Simplified architecture requiring only one API key, and potentially deeper contextual understanding since the language model "sees" the actual image rather than relying on a text label.

---

## ⚙️ Core System Features
Both application implementations share the following core features:
- **Image-Based Analysis**: Users simply upload a photo of a meal to initiate the dietary analysis.
- **Detailed Nutritional Reporting**: Provides an estimated breakdown of calories, macronutrients (Protein, Carbohydrates, Fat), key micronutrients, and general health/allergen insights.
- **Personal Data Tracking**: Local CSV logging allows users to maintain a history of their dietary intake.
- **Accessible GUI**: A straightforward, user-friendly desktop interface built with native Python `Tkinter`.
- **Asynchronous Processing**: API requests run on background threads to ensure the user interface remains responsive during processing.

## 🚀 Getting Started

To run either of the applications, navigate to their respective directories and follow the step-by-step instructions found in their local `README.md` files. 

### General Startup Flow:
1. Navigate to the desired project directory:
   ```bash
   cd nutrition-analyzer-flash
   # OR
   cd nutrition-analyzer-pro
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up a `.env` file in the subdirectory with the necessary API Keys (`CLARIFAI_PAT` and/or `GEMINI_API_KEY`).
5. Launch the application:
   ```bash
   python app.py
   ```
