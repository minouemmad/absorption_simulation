#layer_config.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from materials import MaterialFunctions
from utils import save_settings
import numpy as np


class LayerConfig:
    def __init__(self, root, settings, update_callback):
        self.root = root
        self.settings = settings
        self.update_callback = update_callback
        self.drude_parameters = {}
        self.dbr_layers = []  # DBR layer list
        self.metal_layers = []  # Metal layer list
        self.setup_gui()
    def get_config(self):
        """Return the current configuration as a dictionary."""
        return {
            "substrate": self.substrate_var.get(),
            "dbr_layers": self.dbr_layers,
            "metal_layers": self.metal_layers,
            "drude_parameters": self.drude_parameters,
            "dbr_period": int(self.dbr_period_entry.get()) if self.dbr_period_entry.get().isdigit() else None,
        }

    def setup_gui(self):
        """Set up the GUI layout and elements."""
        # Upload Data Button
        ttk.Button(
            self.root, text="Upload Raw Data", command=self.upload_data
        ).grid(row=4, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

        # Substrate Configuration
        self.setup_substrate_section()

        # DBR Layers Configuration
        self.setup_dbr_section()

        # Metal Layers Configuration
        self.setup_metal_section()

        # Drude Parameters Configuration
        self.parameter_frame = ttk.LabelFrame(self.root, text="Adjust Metal Drude Parameters", padding=10)
        self.parameter_frame.grid(row=3, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

        # Configure resizing
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
            self.root.grid_rowconfigure(i, weight=1)

    def setup_substrate_section(self):
        """Set up the substrate selection section."""
        frame = ttk.LabelFrame(self.root, text="Substrate Configuration", padding=10)
        frame.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

        ttk.Label(frame, text="Select Substrate:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.substrate_var = tk.StringVar(value=self.settings["substrate"])
        ttk.Combobox(
            frame,
            textvariable=self.substrate_var,
            values=["GaSb", "GaAs", "Air"],
            state="readonly",
        ).grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    def setup_dbr_section(self):
        """Set up the DBR layer configuration section."""
        frame = ttk.LabelFrame(self.root, text="Define DBR Layers", padding=10)
        frame.grid(row=1, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

        ttk.Label(frame, text="Material:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.dbr_material_var = tk.StringVar(value="GaSb")
        ttk.Combobox(
            frame,
            textvariable=self.dbr_material_var,
            values=["GaSb", "AlAsSb"],
            state="readonly",
        ).grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(frame, text="Thickness (nm):").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.dbr_thickness_entry = ttk.Entry(frame)
        self.dbr_thickness_entry.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        ttk.Button(frame, text="Add DBR Layer", command=self.add_dbr_layer).grid(row=1, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Clear DBR Layers", command=self.clear_dbr_layers).grid(row=1, column=2, columnspan=2, pady=5)

        ttk.Label(frame, text="Number of Periods:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.dbr_period_entry = ttk.Entry(frame)
        self.dbr_period_entry.insert(0, self.settings["dbr_period"])
        self.dbr_period_entry.grid(row=2, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

        ttk.Button(frame, text="Set DBR Period", command=self.set_dbr_period).grid(row=2, column=3, pady=5)

        self.dbr_layer_list = tk.Listbox(frame, height=5)
        self.dbr_layer_list.grid(row=3, column=0, columnspan=4, sticky="ew", padx=5, pady=5)

    def setup_metal_section(self):
        """Set up the metal layer configuration section."""
        frame = ttk.LabelFrame(self.root, text="Define Metal Layers", padding=10)
        frame.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

        ttk.Label(frame, text="Material:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.metal_material_var = tk.StringVar(value="Au")
        ttk.Combobox(
            frame,
            textvariable=self.metal_material_var,
            values=["Ag", "Al", "Au", "Cu", "Cr", "Ni", "W", "Ti", "Be", "Pd", "Pt"],
            state="readonly",
        ).grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(frame, text="Thickness (nm):").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.metal_thickness_entry = ttk.Entry(frame)
        self.metal_thickness_entry.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        ttk.Button(frame, text="Add Metal Layer", command=self.add_metal_layer).grid(row=1, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Clear Metal Layers", command=self.clear_metal_layers).grid(row=1, column=2, columnspan=2, pady=5)

        self.metal_layer_list = tk.Listbox(frame, height=5)
        self.metal_layer_list.grid(row=2, column=0, columnspan=4, sticky="ew", padx=5, pady=5)

    def upload_data(self):
        """Handle raw data file upload."""
        file_path = filedialog.askopenfilename(
            title="Select Raw Data File",
            filetypes=(("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("All Files", "*.*")),
        )
        if file_path:
            print(f"Selected file: {file_path}")

    def add_dbr_layer(self):
        """Add a DBR layer to the list."""
        thickness = float(self.dbr_thickness_entry.get())
        material = self.dbr_material_var.get()
        layer = [
            thickness,
            "Constant",
            MaterialFunctions.GaSb_ln if material == "GaSb" else MaterialFunctions.AlAsSb_ln,
        ]
        self.dbr_layers.append(layer)
        self.dbr_layer_list.insert(tk.END, f"{material} - {thickness} nm")
        save_settings(self.settings)

    def set_dbr_period(self):
        """Set the DBR period and stack."""
        self.settings["dbr_period"] = int(self.dbr_period_entry.get())
        self.dbr_stack = self.settings["dbr_period"] * self.dbr_layers
        messagebox.showinfo("DBR Stack", f"DBR Stack set with {len(self.dbr_stack)} layers.")
        save_settings(self.settings)

    def clear_dbr_layers(self):
        """Clear all DBR layers."""
        self.dbr_layers.clear()
        self.dbr_layer_list.delete(0, tk.END)
        save_settings(self.settings)

    def add_metal_layer(self):
        """Add a metal layer and initialize its Drude parameters."""
        material = self.metal_material_var.get()
        thickness = self.metal_thickness_entry.get()
        if not thickness.isdigit():
            messagebox.showerror("Error", "Invalid thickness value.")
            return

        self.metal_layer_list.insert(tk.END, f"{material} ({thickness} nm)")
        self.metal_layers.append({"material": material, "thickness": float(thickness)})

        # Initialize Drude parameters
        self.drude_parameters[material] = {"omega_p": 9.03, "f": [0.760, 0.024], "Gamma": [0.053, 0.241], "omega": [0.000, 0.415]}
        self.update_drude_gui()

        self.update_callback()

    def clear_metal_layers(self):
        """Clear all metal layers."""
        self.metal_layers.clear()
        self.metal_layer_list.delete(0, tk.END)
        save_settings(self.settings)

    def update_drude_gui(self):
        """Create widgets for Drude parameters dynamically."""
        for widget in self.parameter_frame.winfo_children():
            widget.destroy()

        row = 0
        for metal, params in self.drude_parameters.items():
            ttk.Label(self.parameter_frame, text=f"{metal} Parameters:").grid(row=row, column=0, sticky="w")
            for i, (param, value) in enumerate(params.items()):
                ttk.Label(self.parameter_frame, text=f"{param}:").grid(row=row, column=i + 1, sticky="w")
                spinbox = ttk.Spinbox(self.parameter_frame, from_=0.0, to=100.0, increment=0.01)
                spinbox.set(value)
                spinbox.grid(row=row, column=i + 2)
                spinbox.bind("<FocusOut>", lambda e, m=metal, p=param: self.update_param(m, p, spinbox))
            row += 1

    def update_param(self, metal, param, spinbox):
        """Update a Drude parameter and trigger simulation update."""
        try:
            value = float(spinbox.get())
            self.drude_parameters[metal][param] = value
            self.update_callback()
        except ValueError:
            messagebox.showerror("Error", "Invalid parameter value.")

    def clear_metal_layers(self):
        self.metal_layers.clear()
        self.metal_layer_list.delete(0, tk.END)
        save_settings(self.settings)

    def setup_metal_parameters(self, frame):
        self.params = {
            "plasma_freq": tk.DoubleVar(value=9.0),
            "collision_freq": tk.DoubleVar(value=0.1)
        }

        tk.Label(frame, text="Plasma Frequency (eV):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.plasma_freq_entry = ttk.Spinbox(frame, textvariable=self.params["plasma_freq"], from_=0.1, to=20.0, increment=0.1, width=10)
        self.plasma_freq_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Collision Frequency (eV):").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.collision_freq_entry = ttk.Spinbox(frame, textvariable=self.params["collision_freq"], from_=0.01, to=5.0, increment=0.01, width=10)
        self.collision_freq_entry.grid(row=1, column=3, padx=5, pady=5)

    def update_metal_parameters(self, event):
        metal = self.metal_var.get()
        # Load preset Drude model parameters based on the metal
        if metal == "Au":
            self.params["plasma_freq"].set(9.0)
            self.params["collision_freq"].set(0.1)
        elif metal == "Ag":
            self.params["plasma_freq"].set(9.1)
            self.params["collision_freq"].set(0.05)
        elif metal == "Al":
            self.params["plasma_freq"].set(15.0)
            self.params["collision_freq"].set(0.15)
        
        self.update_plot_callback(self.calculate_simulated_data())
    def calculate_simulated_data(self):
        # Placeholder for reflectance calculation
        wavelengths = np.linspace(400, 800, 100)
        reflectance = np.random.random(100)  # Replace with real calculation
        return {"wavelength": wavelengths, "reflectance": reflectance}



    def get_layers(self):
        # Substrate layer configuration
        if self.substrate_var.get() == "Air":
            substrate_layer = [[float('nan'), "Constant", [1.0, 0.0]]]  # Ambient air layer
        else:
            substrate_layer = [
                [float('nan'), "Constant", MaterialFunctions.GaSb_ln
 if self.substrate_var.get() == "GaSb" else MaterialFunctions.GaAs_ln
]
            ]

        dbr_stack = self.settings["dbr_period"] * self.dbr_layers
        return dbr_stack, self.metal_layers, substrate_layer
