# # Implementation of subplot and secondary axis
import numpy as np
import matplotlib.pyplot as plt

# Generate sample data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Create figure and axes
fig, ax1 = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

# First subplot
ax1[0].plot(x, y1, 'b-')
ax1[0].set_ylabel('Primary Y Axis 1', color='b')
ax1[0].tick_params('y', colors='b')

# Secondary y-axis for the first subplot
ax1_sec = ax1[0].twinx()
ax1_sec.plot(x, y2, 'r-')
ax1_sec.set_ylabel('Secondary Y Axis 1', color='r')
ax1_sec.tick_params('y', colors='r')

# Second subplot
ax1[1].plot(x, y1**2, 'g-')
ax1[1].set_ylabel('Primary Y Axis 2', color='g')
ax1[1].tick_params('y', colors='g')

# Secondary y-axis for the second subplot
ax2_sec = ax1[1].twinx()
ax2_sec.plot(x, y2**2, 'm-')
ax2_sec.set_ylabel('Secondary Y Axis 2', color='m')
ax2_sec.tick_params('y', colors='m')

# Common x-axis label
plt.xlabel('X Axis')

plt.tight_layout()
plt.show()

