from neuron import h
h.load_file('stdrun.hoc')
from matplotlib import pyplot

## Here I'll try to do the SNNAP example network with NEURON

# morphology and dynamics
soma = h.Section()
soma.insert('hh')
# current clamp
i = h.IClamp(soma(0.5))
i.delay = 2 # ms
i.dur = 0.5 # ms
i.amp = 50 # nA
# recording
t = h.Vector()
v = h.Vector()
t.record(h._ref_t)
v.record(soma(0.5)._ref_v)
# simulation
h.finitialize()
h.continuerun(49.5)
# plotting
pyplot.plot(t, v)
pyplot.xlabel('time (ms)')
pyplot.ylabel('mV')
pyplot.show()