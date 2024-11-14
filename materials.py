#materials.py - Stores refractive index constants.
import numpy as np

# Placeholder refractive index functions; replace with actual models or data arrays.

def GaSb_ln(wavelength):
    """Refractive index model for GaSb as a function of wavelength (in nm)."""
    return 3.96 + 0.01 * (wavelength / 1000)  # Example model, replace with real data

def AlAsSb_ln(wavelength):
    """Refractive index model for AlAsSb as a function of wavelength (in nm)."""
    return 3.1 + 0.02 * (wavelength / 1000)  # Example model, replace with real data

def GaAs_ln(wavelength):
    """Refractive index model for GaAs as a function of wavelength (in nm)."""
    return 3.3 + 0.015 * (wavelength / 1000)  # Example model, replace with real data

# Metal refractive index functions
def Ag_ln(wavelength):
    """Refractive index model for Silver as a function of wavelength (in nm)."""
    return 0.13 + 4.0j  # Simplified example, replace with real data

def Au_ln(wavelength):
    """Refractive index model for Gold as a function of wavelength (in nm)."""
    return 0.16 + 3.5j  # Simplified example, replace with real data

def Al_ln(wavelength):
    """Refractive index model for Aluminum as a function of wavelength (in nm)."""
    return 0.43 + 7.3j  # Simplified example, replace with real data

# Add other materials as needed.
