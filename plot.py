import matplotlib.pyplot as plt

# Read the data from the file
x = []
y = []

with open('out.txt', 'r') as file:
    for line in file:
        # Split each line by comma
        data = line.strip().split(',')
        # Append the values to the respective lists
        x.append(float(data[0]))
        y.append(float(data[1]))

# Plot the data
plt.figure(figsize=(10, 5))
plt.plot(x, y, marker='o', linestyle='-', color='b')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Simple Plot from Data File')
plt.grid(True)
plt.show()
