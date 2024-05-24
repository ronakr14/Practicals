import numpy as np
import matplotlib.pyplot as plt
 
x_vals = np.linspace(0, 10, 100)
y_vals_sin = np.sin(x_vals)
y_vals_exp = np.exp(x_vals)
 
fig, primary_ax = plt.subplots()
 
primary_ax.plot(x_vals, y_vals_sin, 'b-', label='y = sin(x)')
primary_ax.set_xlabel('Primary X axis')
primary_ax.set_ylabel('Y axis', color='b')
primary_ax.tick_params(axis='y', colors='b')
 
secondary_ax = primary_ax.twinx()
 
secondary_ax.plot(x_vals, y_vals_exp, 'r-', label='y = exp(x)')
secondary_ax.set_ylabel('Y axis', color='r')
secondary_ax.tick_params(axis='y', colors='r')
 
extra_ax = primary_ax.twiny()
 
extra_ax.xaxis.set_ticks_position('bottom')
extra_ax.xaxis.set_label_position('bottom')
 
extra_ax.set_xlim(primary_ax.get_xlim())
 
extra_ax.set_xticks(np.linspace(0, 10, 11))
extra_ax.set_xticklabels(['{:.1f}'.format(i) for i in np.linspace(0, 10, 11)])
 
extra_ax.set_xlabel('Secondary X axis')
 
extra_ax.spines['bottom'].set_position(('outward', 40))
 
lines1, labels1 = primary_ax.get_legend_handles_labels()
lines2, labels2 = secondary_ax.get_legend_handles_labels()
primary_ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
 
plt.show()
 
