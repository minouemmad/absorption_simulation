#main.py
# main.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from layer_config import LayerConfig
from plotting import PlotReflectance
from utils import load_settings, save_settings


class LayerStackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Layer Stack Reflectance App")
        self.root.geometry("900x600")

        # Load settings
        self.settings = load_settings()

        # Initialize data variables
        self.raw_data = None
        self.plot = PlotReflectance()

        # Configure layout and components
        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface components."""
        # File upload button for raw data
        self.setup_upload_button()

        # Instruction Label
        tk.Label(
            self.root,
            text="Upload raw data to compare, or define layers to simulate reflectance.",
            font=("Arial", 12)
        ).grid(row=1, column=0, columnspan=3, pady=(5, 5))

        # Layer configuration section
        self.layer_config = LayerConfig(self.root, self.settings, self.update_simulation)

        # Simulate button
        simulate_btn = tk.Button(
            self.root,
            text="Plot Simulated Reflectance",
            command=self.plot_simulation,
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
            font=("Arial", 12)
        )
        simulate_btn.grid(row=0, column=1, pady=(10, 10))

        # Resizable layout
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(2, 20):
            self.root.grid_rowconfigure(i, weight=1)

    def setup_upload_button(self):
        """Set up the file upload button."""
        upload_btn = tk.Button(
            self.root,
            text="Upload Raw Reflectance Data",
            command=self.upload_raw_data,
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
            font=("Arial", 12)
        )
        upload_btn.grid(row=0, column=0, pady=(10, 10))

    def upload_raw_data(self):
        """Handle uploading and loading of raw reflectance data."""
        file_path = filedialog.askopenfilename(
            title="Select Raw Reflectance Data File",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )
        if file_path:
            try:
                self.raw_data = load_raw_data(file_path)

                # Validate data structure
                if not self.raw_data or "wavelength" not in self.raw_data or "reflectance" not in self.raw_data:
                    raise ValueError("Invalid data format. Ensure the file contains 'wavelength' and 'reflectance'.")

                messagebox.showinfo("Success", "Raw reflectance data loaded successfully.")
                self.plot.plot_raw_data(self.raw_data)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def update_simulation(self):
        """Automatically update simulation whenever parameters or layers change."""
        if not self.raw_data:
            return  # Do nothing if raw data is not uploaded yet

        try:
            # Retrieve updated inputs from LayerConfig
            angle, polarization, dbr_stack, metal_layers, substrate_layer = self.layer_config.get_config()
            include_substrate = True
            substrate = self.settings["substrate"]

            # Update the plot
            self.plot.plot_stack(
                angle, polarization, include_substrate, self.raw_data, substrate, dbr_stack, metal_layers
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update simulation: {e}")

    def plot_simulation(self):
        """Plot simulated reflectance without requiring raw data."""
        try:
            angle, polarization, dbr_stack, metal_layers, substrate_layer = self.layer_config.get_config()
            include_substrate = True
            substrate = self.settings["substrate"]
            self.plot.plot_stack(
                angle, polarization, include_substrate, None, substrate, dbr_stack, metal_layers
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to plot simulation: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LayerStackApp(root)
    root.mainloop()
