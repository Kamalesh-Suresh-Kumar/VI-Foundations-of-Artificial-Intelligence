import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import os
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
import threading
import queue

# --- Load Gemini API Key ---
load_dotenv()
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("API key not found in .env file.")
    genai.configure(api_key=api_key)
except Exception as e:
    messagebox.showerror("API Configuration Error", str(e))
    exit()

# --- Backend Functions ---
def get_gemini_analysis_pro(image, quantity_string):
    # Sends image and quantity to Gemini Pro vision model for full analysis.
    model = genai.GenerativeModel('gemini-2.5-pro')

    prompt = f"""
    Analyze the food in this image for the specified portion size. The user has indicated the quantity is '{quantity_string}'.
    If the quantity is in units (e.g., '2 apples'), use your knowledge to estimate the typical weight for the analysis.

    Your response MUST be in this exact markdown format:

    **1. Food Identification:**
    * **Primary food item:** [Name of the dish or main items found in the image]
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
    * **Summary:** [A brief summary of health benefits or considerations based on the identified food.]
    * **Potential Allergens:** [List any potential common allergens based on the identified food.]
    """

    # Send both prompt text AND image
    response = model.generate_content([prompt, image])
    return response.text

def save_analysis_to_csv(image_source, quantity_string, analysis_data):
    """Saves the analysis report to a CSV file."""
    try:
        data_dict = {"Timestamp": [pd.Timestamp.now()], "Image Source": [image_source], "Quantity": [quantity_string], "Report": [analysis_data]}
        df = pd.DataFrame(data_dict)
        csv_path = "nutrition_log_pro.csv" # Separate log file
        df.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path), index=False)
        return f"Analysis saved to {csv_path}"
    except Exception as e:
        return f"Error saving to CSV: {e}"

# --- TKinter GUI Application Class ---
class NutritionAppPro:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Nutrition Analyzer (Pro Version)")
        self.root.geometry("600x800")

        self.image_path = None
        self.image_display = None

        # --- Create Widgets ---
        self.title_label = tk.Label(root, text="AI Nutrition Analyzer", font=("Helvetica", 18, "bold"))
        self.upload_button = tk.Button(root, text="Upload Food Image", command=self.upload_image)
        self.image_label = tk.Label(root)

        self.quantity_frame = tk.Frame(root)
        self.quantity_label = tk.Label(self.quantity_frame, text="Quantity:")
        self.quantity_entry = tk.Entry(self.quantity_frame, width=10)

        self.placeholder_text = "e.g., 150"
        self.add_placeholder()
        self.quantity_entry.bind('<FocusIn>', self.on_entry_click)
        self.quantity_entry.bind('<FocusOut>', self.on_focusout)

        self.unit_options = ["grams", "units/pieces"]
        self.unit_var = tk.StringVar(root)
        self.unit_var.set(self.unit_options[0])
        self.unit_var.trace_add("write", self.update_placeholder)
        self.unit_menu = tk.OptionMenu(self.quantity_frame, self.unit_var, *self.unit_options)

        self.button_frame = tk.Frame(root)
        self.analyze_button = tk.Button(self.button_frame, text="Analyze Nutrition", command=self.start_analysis_thread, font=("Helvetica", 12, "bold"), bg="#007bff", fg="white")
        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_all, font=("Helvetica", 12, "bold"), bg="#e84c4c", fg="white")

        self.result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20)
        self.status_label = tk.Label(root, text="Please upload an image to begin.", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.exit_button = tk.Button(root, text="Exit Application", command=self.on_closing, bg="#dc3545", fg="white")

        # --- Layout Widgets ---
        self.title_label.pack(pady=10)
        self.upload_button.pack(pady=5)
        self.image_label.pack(pady=10)
        self.quantity_frame.pack(pady=5)
        self.quantity_label.pack(side=tk.LEFT, padx=(0, 5))
        self.quantity_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.unit_menu.pack(side=tk.LEFT)
        self.button_frame.pack(pady=10)
        self.analyze_button.pack(side=tk.LEFT, padx=10)
        self.clear_button.pack(side=tk.LEFT, padx=10)
        self.result_text.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)
        self.exit_button.pack(pady=10, side=tk.BOTTOM)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing) # Handle window close
        self.result_queue = queue.Queue() # For thread communication
        self.root.after(100, self.check_queue) # Start checking the queue

    # --- Placeholder and UI Logic Methods ---
    def add_placeholder(self):
        """Adds placeholder text to the quantity entry."""
        self.quantity_entry.insert(0, self.placeholder_text)
        self.quantity_entry.config(fg='grey')

    def on_entry_click(self, event):
        """Clears placeholder on click."""
        if self.quantity_entry.get() == self.placeholder_text:
            self.quantity_entry.delete(0, "end")
            self.quantity_entry.insert(0, '')
            self.quantity_entry.config(fg='black')

    def on_focusout(self, event):
        """Adds placeholder back if entry is empty."""
        if not self.quantity_entry.get():
            self.add_placeholder()

    def update_placeholder(self, *args):
        """Updates placeholder based on unit selection, preserving user input."""
        current_text = self.quantity_entry.get()
        is_placeholder_active = (not current_text or
                                 current_text == "e.g., 150" or
                                 current_text == "e.g., 10")

        new_placeholder = "e.g., 150" if self.unit_var.get() == "grams" else "e.g., 10"

        if is_placeholder_active:
            self.quantity_entry.delete(0, "end")
            self.placeholder_text = new_placeholder # Update internal variable first
            self.add_placeholder()
        else:
             self.placeholder_text = new_placeholder # Keep internal variable consistent

    def clear_all(self):
        """Clears image, result text, and resets quantity entry."""
        self.image_path = None
        self.image_label.config(image='')
        self.image_label.image = None # Prevent garbage collection issues
        self.result_text.delete(1.0, tk.END)
        self.status_label.config(text="Please upload an image to begin.")
        self.quantity_entry.delete(0, "end")
        self.add_placeholder()
        self.root.focus() # Remove focus from entry

    def upload_image(self):
        """Opens file dialog, loads and displays image."""
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if not path:
            return
        self.image_path = path
        try:
            img = Image.open(path)
            img.thumbnail((300, 300)) # Resize for display
            self.image_display = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.image_display)
            self.status_label.config(text=f"Loaded: {os.path.basename(path)}")
            self.result_text.delete(1.0, tk.END)
        except Exception as e:
            messagebox.showerror("Image Error", f"Could not load image: {e}")
            self.image_path = None

    def start_analysis_thread(self):
        """Validates inputs and starts the analysis in a background thread."""
        if not self.image_path:
            messagebox.showwarning("No Image", "Please upload an image first.")
            return

        quantity_value = self.quantity_entry.get()
        if not quantity_value or quantity_value == self.placeholder_text:
            messagebox.showwarning("Invalid Input", "Please enter a quantity.")
            return

        # Validate quantity is numeric
        try:
            numeric_quantity = float(quantity_value)
        except ValueError:
            messagebox.showerror("Invalid Quantity", "Please enter a valid number (e.g., 150 or 2.5).")
            return

        # Format quantity string for the prompt
        selected_unit = self.unit_var.get()
        if selected_unit == "units/pieces":
            unit_text = "unit/piece" if numeric_quantity == 1 else "units/pieces"
            full_quantity_string = f"{quantity_value} {unit_text}"
        else:
            full_quantity_string = f"{quantity_value} {selected_unit}"

        # Disable buttons and start analysis thread
        self.analyze_button.config(state=tk.DISABLED)
        self.upload_button.config(state=tk.DISABLED)
        self.clear_button.config(state=tk.DISABLED)
        self.status_label.config(text="Analyzing... Please wait...")
        self.result_text.delete(1.0, tk.END)
        threading.Thread(target=self.run_analysis, args=(self.image_path, full_quantity_string), daemon=True).start()

    def run_analysis(self, image_path, quantity_string):
        """Calls the Gemini API in a background thread."""
        try:
            img = Image.open(image_path)
            # Call the Gemini function (includes prompt creation)
            analysis_report = get_gemini_analysis_pro(img, quantity_string)
            save_status = save_analysis_to_csv(os.path.basename(image_path), quantity_string, analysis_report)
            self.result_queue.put(("success", analysis_report, save_status))
        except Exception as e:
            # Send error back to the main thread via queue
            self.result_queue.put(("error", str(e), None))

    def check_queue(self):
        """Checks the queue for results from the analysis thread."""
        try:
            status, report, save_msg = self.result_queue.get_nowait()
            if status == "success":
                self.result_text.insert(tk.END, report)
                self.status_label.config(text=save_msg)
            else: # 'error' status
                messagebox.showerror("Analysis Error", report)
                self.status_label.config(text="Analysis failed. Please try again.")

            # Re-enable buttons after success or error
            self.analyze_button.config(state=tk.NORMAL)
            self.upload_button.config(state=tk.NORMAL)
            self.clear_button.config(state=tk.NORMAL)
        except queue.Empty:
            pass # Keep checking
        finally:
            self.root.after(100, self.check_queue) # Schedule next check

    def on_closing(self):
        """Handles window close event."""
        if messagebox.askokcancel("Quit", "Do you want to exit the application?"):
            self.root.destroy()

# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = NutritionAppPro(root)
    root.mainloop()
    