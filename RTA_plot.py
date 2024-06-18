import matplotlib.pyplot as plt
import csv

# Define the paths to your CSV files
reflection_csv = 'data/TiPtAu REFLECTION 2-16-24.CSV'
gold_reflection_csv = 'data/GOLD REFLECTION 2-16-24.CSV'
transmission_csv = 'data/TiPtAu TRANSMISSION 2-16-24.CSV'  # New transmission file

# Customizable axis labels
x_axis_label = 'Wavelength (µm)'
y_axis_label = 'Normalized Amplitude'

# Lists to store the data
x_data = []
y_reflection = []
y_transmission = []
y_absorption = []
y_gold_reflection = []

# Function to read CSV data
def read_csv_data(file_path, x_data, y_data):
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            x_data.append(float(row[0]))
            y_data.append(float(row[1]))

# Read data from the CSV files
read_csv_data(reflection_csv, x_data, y_reflection)
read_csv_data(gold_reflection_csv, [], y_gold_reflection)
read_csv_data(transmission_csv, [], y_transmission)

# Convert wavenumbers to wavelengths in micrometers
wavelengths = [10000 / wavenumber for wavenumber in x_data]

# Normalize the amplitudes
normalized_reflection = [
    y / z if z != 0 else 0.0
    for y, z in zip(y_reflection, y_gold_reflection)
]
normalized_transmission = [
    y / z if z != 0 else 0.0
    for y, z in zip(y_transmission, y_gold_reflection)
]


# Determine y-axis limits based on the data
all_data = normalized_reflection + normalized_transmission
y_min = 0  # Set the minimum y-axis value
y_max = 1.0  # Set the maximum y-axis value
x_max = 6.0  # Set the maximum x-axis value
x_min = 2.5  # Set the minimum x-axis value

# Create the plot
plt.figure(figsize=(10, 6))  # Set the figure size

# Plot the normalized reflection data
plt.plot(wavelengths, normalized_reflection, label='Reflection', linestyle='-', color='red')

# Plot the normalized transmission data
plt.plot(wavelengths, normalized_transmission, label='Transmission', linestyle='-', color='blue')

# Customize axis labels
plt.xlabel(x_axis_label)
plt.ylabel(y_axis_label)

# Customize plot title and grid
plt.title('Reflection and Transmission')
plt.grid(True)  # Add grid lines

# Add a legend
plt.legend()

# Tighten the y/x boundaries
plt.ylim(y_min, y_max)
plt.xlim(x_min, x_max)


# Show the plot
plt.show()
