import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib import pyplot as plt
import numpy as np
import json
import Funcs as MF  # Assuming this is the transfer matrix function module

# Constants for the refractive indices of materials
GaSb_ln = [3.816, 0.0]
AlAsSb_ln = [3.101, 0.0]
GaAs_ln = [3.6, 0.0]  # Placeholder value for GaAs

# Load previous settings if they exist
def load_settings():
    try:
        with open("user_settings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"dbr_layers": [], "dbr_period": 1, "metal_layers": [], "substrate": "GaSb"}

# Save settings to a JSON file
def save_settings():
    settings = {
        "dbr_layers": dbr_layers,
        "dbr_period": int(dbr_period_entry.get()),
        "metal_layers": metal_layers,
        "substrate": substrate_var.get()
    }
    with open("user_settings.json", "w") as f:
        json.dump(settings, f)

settings = load_settings()

# GUI setup
root = tk.Tk()
root.title("Layer Stack Configuration")

# Lists to store user-defined DBR and metal layers
dbr_layers = settings["dbr_layers"]
metal_layers = settings["metal_layers"]

# DBR Layer Functions
def add_dbr_layer():
    thickness = float(dbr_thickness_entry.get())
    material = dbr_material_var.get()
    layer = [thickness, "Constant", GaSb_ln if material == "GaSb" else AlAsSb_ln]
    dbr_layers.append(layer)
    dbr_layer_list.insert(tk.END, f"{material} - {thickness} nm")
    save_settings()

def set_dbr_period():
    global dbr_stack
    dbr_stack = int(dbr_period_entry.get()) * dbr_layers
    messagebox.showinfo("DBR Stack", f"DBR Stack set with {len(dbr_stack)} layers.")
    save_settings()

def clear_dbr_layers():
    dbr_layers.clear()
    dbr_layer_list.delete(0, tk.END)
    save_settings()

# Metal Layer Functions
def add_metal_layer():
    thickness = float(metal_thickness_entry.get())
    metal = metal_material_var.get()
    layer = [thickness, "Lorentz-Drude", [metal]]
    metal_layers.append(layer)
    metal_layer_list.insert(tk.END, f"{metal} - {thickness} nm")
    save_settings()

def clear_metal_layers():
    metal_layers.clear()
    metal_layer_list.delete(0, tk.END)
    save_settings()

# Plot Function
def plot_stack():
    global substrate_layer
    substrate_material = substrate_var.get()
    substrate_layer = [[np.nan, "Constant", GaSb_ln if substrate_material == "GaSb" else GaAs_ln]]
    Ls_structure = [[np.nan, "Constant", [1.0, 0.0]]] + metal_layers + [[239., "Constant", AlAsSb_ln]]+ dbr_stack + substrate_layer
    Ls_structure = Ls_structure[::-1]

    nlamb = 3500
    x = np.linspace(2.5, 15, nlamb) * 1000
    incang = 0 * np.pi / 180 * np.ones(x.size) # Incident angle (normal incidence)

    rs, rp, Ts, Tp = MF.calc_rsrpTsTp(incang, Ls_structure, x)
    R0 = (abs(rs))**2
    T0 = np.real(Ts)
    Abs1 = 1.0 - R0 - T0

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(x / 1000, R0, label='Reflectance')
    ax1.set_xlabel('Wavelength (μm)', size=12)
    ax1.set_ylabel('Reflectance', size=12)
    ax1.set_title('Reflectance of Custom Layer Stack', size=16)
    ax1.legend()
    ax1.grid(alpha=0.2)
    plt.tight_layout()
    plt.show()
    save_settings()

# Layout
tk.Label(root, text="Define DBR Layers").grid(row=0, column=0, columnspan=3)
dbr_material_var = tk.StringVar(value="GaSb")
dbr_material_menu = ttk.Combobox(root, textvariable=dbr_material_var, values=["GaSb", "AlAsSb"])
dbr_material_menu.grid(row=1, column=0)
tk.Label(root, text="Thickness (nm):").grid(row=1, column=1)
dbr_thickness_entry = tk.Entry(root)
dbr_thickness_entry.grid(row=1, column=2)
add_dbr_btn = tk.Button(root, text="Add DBR Layer", command=add_dbr_layer)
add_dbr_btn.grid(row=2, column=0, columnspan=3)
tk.Label(root, text="Number of Periods:").grid(row=3, column=0)
dbr_period_entry = tk.Entry(root)
dbr_period_entry.insert(0, settings["dbr_period"])
dbr_period_entry.grid(row=3, column=1, columnspan=2)
dbr_period_btn = tk.Button(root, text="Set DBR Period", command=set_dbr_period)
dbr_period_btn.grid(row=4, column=0, columnspan=3)
clear_dbr_btn = tk.Button(root, text="Clear DBR Layers", command=clear_dbr_layers)
clear_dbr_btn.grid(row=5, column=0, columnspan=3)
dbr_layer_list = tk.Listbox(root, height=5)
dbr_layer_list.grid(row=6, column=0, columnspan=3)

tk.Label(root, text="Define Metal Layers").grid(row=7, column=0, columnspan=3)
metal_material_var = tk.StringVar(value="Au")
metal_material_menu = ttk.Combobox(root, textvariable=metal_material_var, values=["Ag", "Al", "Au", "Cu", "Cr", "Ni", "W", "Ti", "Be", "Pd", "Pt"])
metal_material_menu.grid(row=8, column=0)
tk.Label(root, text="Thickness (nm):").grid(row=8, column=1)
metal_thickness_entry = tk.Entry(root)
metal_thickness_entry.grid(row=8, column=2)
add_metal_btn = tk.Button(root, text="Add Metal Layer", command=add_metal_layer)
add_metal_btn.grid(row=9, column=0, columnspan=3)
clear_metal_btn = tk.Button(root, text="Clear Metal Layers", command=clear_metal_layers)
clear_metal_btn.grid(row=10, column=0, columnspan=3)
metal_layer_list = tk.Listbox(root, height=5)
metal_layer_list.grid(row=11, column=0, columnspan=3)

tk.Label(root, text="Select Substrate").grid(row=12, column=0, columnspan=3)
substrate_var = tk.StringVar(value=settings["substrate"])
substrate_menu = ttk.Combobox(root, textvariable=substrate_var, values=["GaSb", "GaAs"])
substrate_menu.grid(row=13, column=0, columnspan=3)

plot_btn = tk.Button(root, text="Plot Reflectance", command=plot_stack)
plot_btn.grid(row=14, column=0, columnspan=3)

root.mainloop()
