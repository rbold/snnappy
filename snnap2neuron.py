
from neuron import h
# h.nrn_load_dll("nrnmech.dll")

mt = h.MechanismType(1)
mname  = h.ref('')
# for i in range(int(mt.count())):
#     mt.select(i)
#     mt.selected(mname)
#     print(mname[0])

mt.select('snnap_ionic1')
mt.selected(mname)
print(mname)

# morphology and dynamics
soma = h.Section()
c1 = h.snnap_ionic1(soma(0.5))
c1.e          =   40.0   # (mV)
c1.gmax       =    2.4   # (uS)
c1.p          =    3

c1.hA         =  -45.0   # (mV)
c1.sA         =   -8.0   # (mV)

c1.hB         =  -40.0   # (mV)
c1.sB         =    1.2   # (mV)
c1.pB         =    1
c1.Bmin       =    0

c1.tauAmin    =  400.    # (ms)
c1.tauAmax    =  400.    # (ms)
c1.htauA      =    0     # (mV)
c1.stauA      =    1     # (mV)

c1.tauBmin    = 4000.    # (ms)
c1.tauBmax    = 4000.    # (ms)
c1.htauB      =    0     # (mV)
c1.stauB      =    1     # (mV)

soma.CVode.dt = 0.002