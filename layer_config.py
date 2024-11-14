import tkinter as tk
from tkinter import ttk, messagebox
from materials import GaSb_ln, AlAsSb_ln, GaAs_ln
from utils import save_settings

class LayerConfig:
    def __init__(self, root, settings):
        self.root = root
        self.settings = settings
        self.dbr_layers = settings["dbr_layers"]
        self.metal_layers = settings["metal_layers"]
        
        self.setup_dbr_layers()
        self.setup_metal_layers()
        self.setup_substrate_selection()
        
    def setup_dbr_layers(self):
        tk.Label(self.root, text="Define DBR Layers").grid(row=0, column=0, columnspan=3)
        self.dbr_material_var = tk.StringVar(value="GaSb")
        ttk.Combobox(self.root, textvariable=self.dbr_material_var, values=["GaSb", "AlAsSb"]).grid(row=1, column=0)
        tk.Label(self.root, text="Thickness (nm):").grid(row=1, column=1)
        self.dbr_thickness_entry = tk.Entry(self.root)
        self.dbr_thickness_entry.grid(row=1, column=2)
        tk.Button(self.root, text="Add DBR Layer", command=self.add_dbr_layer).grid(row=2, column=0, columnspan=3)
        
        tk.Label(self.root, text="Number of Periods:").grid(row=3, column=0)
        self.dbr_period_entry = tk.Entry(self.root)
        self.dbr_period_entry.insert(0, self.settings["dbr_period"])
        self.dbr_period_entry.grid(row=3, column=1, columnspan=2)
        tk.Button(self.root, text="Set DBR Period", command=self.set_dbr_period).grid(row=4, column=0, columnspan=3)
        
        tk.Button(self.root, text="Clear DBR Layers", command=self.clear_dbr_layers).grid(row=5, column=0, columnspan=3)
        self.dbr_layer_list = tk.Listbox(self.root, height=5)
        self.dbr_layer_list.grid(row=6, column=0, columnspan=3)
        
    def setup_metal_layers(self):
        tk.Label(self.root, text="Define Metal Layers").grid(row=7, column=0, columnspan=3)
        self.metal_material_var = tk.StringVar(value="Au")
        ttk.Combobox(self.root, textvariable=self.metal_material_var, values=["Ag", "Al", "Au", "Cu", "Cr", "Ni", "W", "Ti", "Be", "Pd", "Pt"]).grid(row=8, column=0)
        tk.Label(self.root, text="Thickness (nm):").grid(row=8, column=1)
        self.metal_thickness_entry = tk.Entry(self.root)
        self.metal_thickness_entry.grid(row=8, column=2)
        tk.Button(self.root, text="Add Metal Layer", command=self.add_metal_layer).grid(row=9, column=0, columnspan=3)
        tk.Button(self.root, text="Clear Metal Layers", command=self.clear_metal_layers).grid(row=10, column=0, columnspan=3)
        self.metal_layer_list = tk.Listbox(self.root, height=5)
        self.metal_layer_list.grid(row=11, column=0, columnspan=3)
        
    def setup_substrate_selection(self):
        tk.Label(self.root, text="Select Substrate").grid(row=12, column=0, columnspan=3)
        self.substrate_var = tk.StringVar(value=self.settings["substrate"])
        ttk.Combobox(self.root, textvariable=self.substrate_var, values=["GaSb", "GaAs"]).grid(row=13, column=0, columnspan=3)
        
    def add_dbr_layer(self):
        thickness = float(self.dbr_thickness_entry.get())
        material = self.dbr_material_var.get()
        layer = [thickness, "Constant", GaSb_ln if material == "GaSb" else AlAsSb_ln]
        self.dbr_layers.append(layer)
        self.dbr_layer_list.insert(tk.END, f"{material} - {thickness} nm")
        save_settings(self.settings)
    
    def set_dbr_period(self):
        self.settings["dbr_period"] = int(self.dbr_period_entry.get())
        self.dbr_stack = self.settings["dbr_period"] * self.dbr_layers
        messagebox.showinfo("DBR Stack", f"DBR Stack set with {len(self.dbr_stack)} layers.")
        save_settings(self.settings)
        
    def clear_dbr_layers(self):
        self.dbr_layers.clear()
        self.dbr_layer_list.delete(0, tk.END)
        save_settings(self.settings)
        
    def add_metal_layer(self):
        thickness = float(self.metal_thickness_entry.get())
        metal = self.metal_material_var.get()
        layer = [thickness, "Lorentz-Drude", [metal]]
        self.metal_layers.append(layer)
        self.metal_layer_list.insert(tk.END, f"{metal} - {thickness} nm")
        save_settings(self.settings)
        
    def clear_metal_layers(self):
        self.metal_layers.clear()
        self.metal_layer_list.delete(0, tk.END)
        save_settings(self.settings)
    
    def get_layers(self):
        substrate_layer = [[float('nan'), "Constant", GaSb_ln if self.substrate_var.get() == "GaSb" else GaAs_ln]]
        dbr_stack = self.settings["dbr_period"] * self.dbr_layers
        return dbr_stack, self.metal_layers, substrate_layer
