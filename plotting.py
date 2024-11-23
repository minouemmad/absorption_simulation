#plotting.py - Manages the reflectance calculation and plotting.
import numpy as np
import matplotlib.pyplot as plt
from materials import MaterialFunctions as MF

class PlotReflectance:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

    def plot_raw_data(self, raw_data):
        wavelengths = raw_data['wavelength']
        reflectance = raw_data['reflectance']

        self.ax.clear()
        self.ax.plot(wavelengths, reflectance, label="Raw Data", linestyle='--', color='blue')
        self.ax.set_xlabel("Wavelength (nm)")
        self.ax.set_ylabel("Reflectance")
        self.ax.legend()
        plt.show()

    def plot_stack(self, angle, polarization, include_substrate, raw_data, substrate, dbr_stack, metal_layers):
        wavelengths, simulated_reflectance = self.calculate_reflectance(angle, polarization)

        self.ax.clear()
        if raw_data:
            self.ax.plot(raw_data["wavelength"], raw_data["reflectance"], label="Raw Data", linestyle="--", color="blue")
        self.ax.plot(wavelengths, simulated_reflectance, label="Simulated Reflectance", color="red")
        self.ax.set_xlabel("Wavelength (nm)")
        self.ax.set_ylabel("Reflectance")
        self.ax.legend()
        plt.show()


    def calculate_reflectance(self, angle, polarization):
        # Placeholder for reflectance calculation
        wavelengths = [400, 500, 600, 700, 800]
        simulated_reflectance = [0.5, 0.6, 0.7, 0.6, 0.5]
        return wavelengths, simulated_reflectance
    