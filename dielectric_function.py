import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
from scipy import integrate
from scipy.interpolate import interp1d  # Import interpolation function
import pandas as pd

# Define the models
MODELS = {
    'Gaussian': {  
        'parameter': ['Amp', 'En', 'Br'],
        'defaults': [1, 3, 0.2],
        'function': lambda eV, Amp, En, Br: Amp * np.exp(-((eV-En)/(Br/(2*np.sqrt(np.log(2)))))**2) - Amp * np.exp(-((eV+En)/(Br/(2*np.sqrt(np.log(2)))))**2)
    },
    'Drude':  {  
        'parameter': ['Amp', 'Br'],
        'defaults': [1, 0.2],
        'function': lambda eV, Amp, Br: (Amp*Br)/(eV**2 + 1j * Br * eV)
    },
    'Lorentz':  {  
        'parameter': ['Amp', 'En', 'Br'],
        'defaults': [1, 3, 0.2],
        'function': lambda eV, Amp, En, Br: (Amp*Br*En)/(En**2 - eV**2 - 1j * Br * eV)
    },  
    'Tauc-Lorentz':  {  
        'parameter': ['Amp', 'En', 'C', 'Eg'],
        'defaults': [20, 4, 0.5, 3.5],
        'function': lambda eV, Amp, En, C, Eg: (Amp*C*En*(eV-Eg)**2)/(eV*((eV**2-En**2)**2+C**2*eV**2))
    },
    'Cody-Lorentz':  {  
        'parameter': ['Amp', 'En', 'Br', 'Eg', 'Ep', 'Et', 'Eu'],
        'defaults': [20, 4, 0.1, 2.5, 1, 0, 0.5],
        'function': [lambda eV, Amp, En, Br, Eg, Ep, Et, Eu: (((eV-Eg)**2)/((eV-Eg)**2+Ep**2)) * (Amp*En*Br*eV)/((eV**2-En**2)**2+Br**2*eV**2),
                     lambda eV, Amp, En, Br, Eg, Ep, Et, Eu: (Et*(((eV-Eg)**2)/((eV-Eg)**2+Ep**2)) * (Amp*En*Br*eV)/((eV**2-En**2)**2+Br**2*eV**2)/eV) * np.exp((eV-Eg-Et)/Eu)]
    }
}

def calcFunction(dielectricFunction):
    eV = np.linspace(dielectricFunction['spectral range'][0], dielectricFunction['spectral range'][1], 100)
    dielectricFunction['wvl'] = 1239.941 / eV
    e = dielectricFunction['e0']
   
    for osci in dielectricFunction['oscillators']:
        if osci['active']:
            name = osci['name']
            params = osci['values']
            model = MODELS[name]['function']
            if name == 'Cody-Lorentz':
                e2_osci = np.zeros(len(eV))
                e2_func1 = model[0](eV, *params)
                e2_func2 = model[1](eV, *params)
                e2_osci[eV > params[3] + params[5]] = e2_func1[eV > params[3] + params[5]]
                e2_osci[eV <= params[3] + params[5]] = e2_func2[eV <= params[3] + params[5]]
            elif name == 'Tauc-Lorentz':
                e2_osci = np.zeros(len(eV))
                e2_func = model(eV, *params)
                e2_osci[eV > params[3]] = e2_func[eV > params[3]]
            else:
                e2_osci = model(eV, *params)
               
            e1_osci = KKR(e2_osci, eV)
            e_osci = e1_osci + 1j * e2_osci
            e += e_osci
   
    e1 = np.real(e)
    e2 = np.imag(e)
    dielectricFunction['n'] = (0.5 * (e1 + np.sqrt(e1**2 + e2**2)))**0.5
    dielectricFunction['k'] = (0.5 * (-e1 + np.sqrt(e1**2 + e2**2)))**0.5
   
    return e1, e2, dielectricFunction, eV

def KKR(e2, eV):
    E = eV
    e1 = np.zeros(len(eV))
    e1[0] = 1 + (2 / np.pi) * integrate.trapz(E[1:-1] * e2[1:-1] / (E[1:-1]**2 - E[0])) * (E[3] - E[2])
    for i in range(1, len(E)):
        e1_part1 = integrate.trapz(E[0:i-1] * e2[0:i-1] / (E[0:i-1]**2 - E[i]**2))
        e1_part2 = integrate.trapz(E[i+1:-1] * e2[i+1:-1] / (E[i+1:-1]**2 - E[i]**2))
        e1[i] = 1 + (2 / np.pi) * (e1_part1 + e1_part2) * (E[3] - E[2])
    return e1

# Load the observed spectrum
observed_wavelengths = np.loadtxt('observed_spectrum.csv', delimiter=',', usecols=0)
observed_spectrum = np.loadtxt('observed_spectrum.csv', delimiter=',')

# Example function to fit the observed reflection spectrum
def fit_reflection_spectrum(dielectricFunction, observed_wavelengths, observed_spectrum):
    def error_function(params):
        dielectricFunction['oscillators'][0]['values'] = params
        _, _, _, eV = calcFunction(dielectricFunction)
        
        # Interpolate observed_spectrum to the eV values of the calculated_spectrum
        interp_func = interp1d(observed_wavelengths, observed_spectrum, kind='linear', fill_value='extrapolate')
        interpolated_spectrum = interp_func(dielectricFunction['wvl'])

        calculated_spectrum = dielectricFunction['n']  # Assuming the reflection spectrum can be represented by n
        return np.sum((interpolated_spectrum - calculated_spectrum)**2)

    initial_params = dielectricFunction['oscillators'][0]['values']
    result = opt.minimize(error_function, initial_params, method='Nelder-Mead')
    return result.x

# Sample dielectric function structure
dielectricFunction = {
    'e0': 1,
    'spectral range': [0.1, 6],
    'oscillators': [
        {'name': 'Drude', 'values': [1, 0.2], 'active': True}
    ]
}

# Fit the reflection spectrum
fitted_params = fit_reflection_spectrum(dielectricFunction, observed_wavelengths, observed_spectrum)
dielectricFunction['oscillators'][0]['values'] = fitted_params

# Calculate the final fitted function
e1, e2, dielectricFunction, eV = calcFunction(dielectricFunction)


# Interpolate observed_spectrum to the eV values of the calculated_spectrum
interp_func = interp1d(observed_wavelengths, observed_spectrum, kind='linear', fill_value='extrapolate')
interpolated_spectrum = interp_func(dielectricFunction['wvl'])

# Plotting the results
plt.plot(dielectricFunction['wvl'], interpolated_spectrum, label='Observed Spectrum')
plt.plot(dielectricFunction['wvl'], dielectricFunction['n'], label='Fitted Spectrum')
plt.xlabel('Wavelength')
plt.ylabel('Reflection Spectrum')
plt.legend()
plt.show()


# Plotting the results
plt.plot(eV, observed_spectrum, label='Observed Spectrum')
plt.plot(eV, dielectricFunction['n'], label='Fitted Spectrum')
plt.xlabel('Wavelength')
plt.ylabel('Reflection Spectrum')
plt.legend()
plt.show()