import numpy as np
import matplotlib.pyplot as plt
from Funcs import calc_rsrpTsTp
def prompt_user():
    # Prompt user for input
    layers_str = input("Enter the structure of layers (array of layer names): ")
    layers = eval(layers_str)  # Convert string input to list
    
    # Collect other inputs
    nlamb = int(input("Enter the number of wavelength points: "))
    start_wavelength = float(input("Enter the start wavelength (nm): "))
    end_wavelength = float(input("Enter the end wavelength (nm): "))
    thickness = float(input("Enter the thickness of layers: "))
    refractive_index = float(input("Enter the refractive index: "))
    is_semi_infinite = input("Is it a semi-infinite substrate? (y/n): ")
    angle_of_incidence = float(input("Enter the angle of incidence (degrees): "))
    
    # Generate wavelength array
    x = np.linspace(start_wavelength, end_wavelength, nlamb)
    
    return layers, x, thickness, refractive_index, is_semi_infinite, angle_of_incidence

if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    from Funcs import calc_rsrpTsTp

    # Prompt user for input
    layers, x, thickness, refractive_index, is_semi_infinite, angle_of_incidence = prompt_user()
    
    # Perform calculations
    incang = np.deg2rad(angle_of_incidence) * np.ones(x.size)
    rs, rp, Ts, Tp = calc_rsrpTsTp(incang, layers, x)
    R = np.abs(rs) ** 2 if is_semi_infinite == 'n' else np.abs(rp) ** 2

    # Plot reflectance vs wavelength
    plt.figure()
    plt.plot(x, R)
    plt.title('Reflectance vs Wavelength')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Reflectance')
    plt.show()