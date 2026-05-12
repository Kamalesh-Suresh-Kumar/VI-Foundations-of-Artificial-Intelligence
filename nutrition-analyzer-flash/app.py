import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import os
import pandas as pd
from dotenv import load_dotenv
import threading
import queue

# Import API functions
from ai_pipelines import identify_food_from_image, generate_report_from_name

# --- Load API Keys ---
load_dotenv()

# --- TKinter GUI Application Class ---
class NutritionAppFlash:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Nutrition Analyzer (Flash Version)")
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
        self.result_text.delete(1.0, tk.END)
        threading.Thread(target=self.run_analysis, args=(self.image_path, full_quantity_string), daemon=True).start()

    def run_analysis(self, image_path, quantity_string):
        """Calls Clarifai API then Gemini API in a background thread."""
        try:
            # Step 1: Identify food via Clarifai
            self.result_queue.put(("status", "Step 1/2: Identifying food via Clarifai API..."))
            food_name = identify_food_from_image(image_path) # From ai_pipelines.py

            # Step 2: Generate report via Gemini
            self.result_queue.put(("status", f"Step 2/2: Generating report for {food_name.title()} via Gemini API..."))
            analysis_report = generate_report_from_name(food_name, quantity_string) # From ai_pipelines.py

            # Save results
            save_status = self.save_analysis_to_csv(os.path.basename(image_path), quantity_string, analysis_report)
            self.result_queue.put(("success", analysis_report, save_status))

        except Exception as e:
            # Send error back to the main thread via queue
            self.result_queue.put(("error", str(e)))

    def check_queue(self):
        """Checks the queue for results from the analysis thread."""
        try:
            status, *data = self.result_queue.get_nowait()

            if status == "status":
                self.status_label.config(text=data[0]) # Update status label

            elif status == "success":
                report, save_msg = data
                self.result_text.insert(tk.END, report)
                self.status_label.config(text=save_msg)
                # Re-enable buttons on success
                self.analyze_button.config(state=tk.NORMAL)
                self.upload_button.config(state=tk.NORMAL)
                self.clear_button.config(state=tk.NORMAL)

            else: # 'error' status
                error_msg = data[0]
                messagebox.showerror("Analysis Error", error_msg)
                self.status_label.config(text="Analysis failed.")
                # Re-enable buttons on error
                self.analyze_button.config(state=tk.NORMAL)
                self.upload_button.config(state=tk.NORMAL)
                self.clear_button.config(state=tk.NORMAL)
        except queue.Empty:
            pass # Keep checking
        finally:
            self.root.after(100, self.check_queue) # Schedule next check

    def save_analysis_to_csv(self, image_source, quantity_string, analysis_data):
        """Saves the analysis report to a CSV file."""
        try:
            data_dict = {"Timestamp": [pd.Timestamp.now()], "Image Source": [image_source], "Quantity": [quantity_string], "Report": [analysis_data]}
            df = pd.DataFrame(data_dict)
            csv_path = "nutrition_log_flash.csv" # Separate log file
            df.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path), index=False)
            return f"Analysis saved to {csv_path}"
        except Exception as e:
            return f"Error saving to CSV: {e}"

    def on_closing(self):
        """Handles window close event."""
        if messagebox.askokcancel("Quit", "Do you want to exit the application?"):
            self.root.destroy()

# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = NutritionAppFlash(root)
    root.mainloop()
    