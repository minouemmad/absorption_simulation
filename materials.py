#materials.py - Stores refractive index constants.
import numpy as np

class MaterialFunctions:
    """Class to store refractive index models for different materials."""

    @staticmethod
    def GaSb_ln(wavelength):
        """Refractive index model for GaSb as a function of wavelength (in nm)."""
        return 3.96 + 0.01 * (wavelength / 1000)  # Example model, replace with real data

    @staticmethod
    def AlAsSb_ln(wavelength):
        """Refractive index model for AlAsSb as a function of wavelength (in nm)."""
        return 3.1 + 0.02 * (wavelength / 1000)  # Example model, replace with real data

    @staticmethod
    def GaAs_ln(wavelength):
        """Refractive index model for GaAs as a function of wavelength (in nm)."""
        return 3.3 + 0.015 * (wavelength / 1000)
