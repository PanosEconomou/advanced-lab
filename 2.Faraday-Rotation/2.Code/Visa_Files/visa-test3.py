from oscillovisa import *
import matplotlib.pyplot as plt

inst = get_intstrunment(VERBOSE=True)
v,t, _ = get_data(inst)

plt.plot(t,v)
plt.show()