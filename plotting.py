#plotting.py - Manages the reflectance calculation and plotting.
import numpy as np
import matplotlib.pyplot as plt
import Funcs as MF
from materials import AlAsSb_ln

class PlotReflectance:
    def __init__(self, dbr_stack=None, metal_layers=None, substrate_layer=None):
        self.dbr_stack = dbr_stack
        self.metal_layers = metal_layers
        self.substrate_layer = substrate_layer

    def plot_raw_data(self, raw_data):
        wavelengths = raw_data['wavelength']
        reflectance = raw_data['reflectance']
        
        plt.plot(wavelengths, reflectance, label="Raw Data", linestyle='--', color='blue')
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Reflectance")
        plt.legend()
        plt.show()  # Show plot immediately after raw data is uploaded

    def plot_stack(self, angle, polarization):
        # Simulated reflectance data plotting
        wavelengths, simulated_reflectance = self.calculate_reflectance(angle, polarization)
        
        plt.plot(wavelengths, simulated_reflectance, label="Simulated Reflectance", color='red')
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Reflectance")
        plt.legend()
        plt.show()
    
    def calculate_reflectance(self, angle, polarization):
        # Placeholder for reflectance calculation
        wavelengths = [400, 500, 600, 700, 800]
        simulated_reflectance = [0.5, 0.6, 0.7, 0.6, 0.5]
        return wavelengths, simulated_reflectance