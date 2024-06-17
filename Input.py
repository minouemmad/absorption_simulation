import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from Funcs import calc_rsrpTsTp
from LD import *

class LayerInput:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.layer_list = []

        self.material_var = tk.StringVar()
        self.thickness_var = tk.StringVar()
        self.repeat_var = tk.StringVar()

        self.materials = ["Ag", "Al", "Au", "Cu", "Cr", "Ni", "W", "Ti", "Be", "Pd", "Pt"]

        self.init_ui()

    def init_ui(self):
        self.layer_table = ttk.Treeview(self.frame, columns=("Material", "Thickness (nm)", "Repeats"), show='headings')
        self.layer_table.heading("Material", text="Material")
        self.layer_table.heading("Thickness (nm)", text="Thickness (nm)")
        self.layer_table.heading("Repeats", text="Repeats")
        self.layer_table.pack(fill=tk.BOTH, expand=True, pady=10)

        input_frame = ttk.Frame(self.frame)
        input_frame.pack(fill=tk.X, pady=5)

        ttk.Label(input_frame, text="Material").grid(row=0, column=0, padx=5, pady=5)
        self.material_entry = ttk.Combobox(input_frame, textvariable=self.material_var, values=self.materials)
        self.material_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Thickness (nm)").grid(row=0, column=2, padx=5, pady=5)
        self.thickness_entry = ttk.Entry(input_frame, textvariable=self.thickness_var)
        self.thickness_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Repeats").grid(row=0, column=4, padx=5, pady=5)
        self.repeat_entry = ttk.Entry(input_frame, textvariable=self.repeat_var)
        self.repeat_entry.grid(row=0, column=5, padx=5, pady=5)

        ttk.Button(input_frame, text="Add Layer", command=self.add_layer).grid(row=0, column=6, padx=5, pady=5)
        ttk.Button(input_frame, text="Calculate and Plot", command=self.plot_rta).grid(row=0, column=7, padx=5, pady=5)

    def add_layer(self):
        material = self.material_var.get()
        thickness = self.thickness_var.get()
        repeats = self.repeat_var.get()

        if material and thickness and repeats:
            self.layer_list.append((material, float(thickness), int(repeats)))
            self.layer_table.insert('', 'end', values=(material, thickness, repeats))
            self.material_var.set('')
            self.thickness_var.set('')
            self.repeat_var.set('')
        else:
            messagebox.showwarning("Input Error", "Please provide all details for the layer.")

    def get_layers(self):
        return self.layer_list

    def plot_rta(self):
        layers = self.get_layers()
        if not layers:
            messagebox.showwarning("Input Error", "Please add at least one layer.")
            return

        # Convert layer list to required format for calculation
        structure = self.build_structure(layers)

        # Define wavelength range
        nlamb = 301
        x_microns = np.linspace(0, 15, nlamb)  # from 0 to 15 microns
        x = x_microns * 1e3  # convert to nm for calculations

        # Define incidence angle (in radians)
        incang = 10 * np.pi / 180 * np.ones(x.size)

        # Calculate RTA
        rs, rp, Ts, Tp = calc_rsrpTsTp(incang, structure, x)
        Rs = np.abs(rs) ** 2
        Rp = np.abs(rp) ** 2
        As = 1 - Rs - Ts  # Absorption for s-polarization
        Ap = 1 - Rp - Tp  # Absorption for p-polarization

        self.plot_results(x_microns, Rs, Rp, Ts, Tp, As, Ap)

    def build_structure(self, layers):
        structure = [[np.nan, 'Constant', [1.0, 0.0]]]  # Air at the start
        for material, thickness, repeats in layers:
            for _ in range(repeats):
                if material in self.materials:
                    ld_material = LD(np.array([400, 800]) * 1e-9, material, model='D')  # Example wavelengths
                    n = ld_material.n[0]
                    k = ld_material.k[0]
                    structure.append([thickness, 'Drude', [n**2 - k**2, 2 * n * k, 1.34e13]])  # Example parameters
                else:
                    messagebox.showwarning("Material Error", f"Material {material} not recognized. Defaulting to 1+0j.")
                    structure.append([thickness, 'Constant', [1.0, 0.0]])
        structure.append([np.nan, 'Constant', [1.0, 0.0]])  # Air at the end
        return structure

    def plot_results(self, x_microns, Rs, Rp, Ts, Tp, As, Ap):
        plt.figure()
        plt.plot(x_microns, Rs, 'k', label='Reflectance - s-pol')
        plt.plot(x_microns, Rp, 'r', label='Reflectance - p-pol')
        plt.plot(x_microns, Ts, 'k', label='Transmittance - s-pol')
        plt.plot(x_microns, Tp, 'r', label='Transmittance - p-pol')
        plt.plot(x_microns, As, 'k', label='Absorbance - s-pol')
        plt.plot(x_microns, Ap, 'r', label='Absorbance - p-pol')
        plt.xlabel('Wavelength (microns)')
        plt.ylabel('Reflectance Coefficient')
        plt.title('RTA vs Wavelength')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Layer Structure Input")
    LayerInput(root)
    root.mainloop()
