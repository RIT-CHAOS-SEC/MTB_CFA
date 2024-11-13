import matplotlib.pyplot as plt
import numpy as np

# Data for the template
algorithms = ['Ultrasonic', 'Geiger', 'Syringe', 'Temperature','GPS','prime','crc32','sglib-binsearch']
methods = ['Method A', 'Method B']
values = np.array([
    [56, 2020],  # Algorithm 1 scores for Method A and Method B
    [186, 2880],  # Algorithm 2 scores for Method A and Method B
    [1400, 49360],
    [1212, 11512],
    [2596, 8400],
    [5216, 10392],
    [8204, 20464],
    [12900, 24224]   # Algorithm 3 scores for Method A and Method B
])

# Setting up bar positions and width
x = np.arange(len(algorithms))
width = 0.35

# Updating the second bar to have a hatched pattern instead of a solid color

fig, ax = plt.subplots()
bars1 = ax.bar(x - width/2, values[:, 0], width, color='black', label='Instrumentation Based CFA')
bars2 = ax.bar(x + width/2, values[:, 1], width, color='white', edgecolor='black', hatch='//', label='Naive MTB Based CFA')

# Adding labels and title
# ax.set_xlabel('Algorithms')
ax.set_ylabel('CFLog Size (Bytes)')
# ax.set_title('Comparison of Two Methods Across Algorithms')
ax.set_xticks(x)
ax.set_xticklabels(algorithms)
ax.legend()
#rotate x-axis labels
plt.xticks(rotation=25)

# Display the plot
plt.show()


