from neuron import h, gui
h.load_file('stdrun.hoc')
from matplotlib import pyplot
import snnappy
import numpy as np

## Here I'll try to do the SNNAP example generic cell with NEURON
## Try to just copy the simulation from generic_cell_01.smu.ing

t = snnappy.snnapsim()
t.from_ing("generic_cell_01.smu.ing")

# create NEURON versions of SNNAP neurons
cells = []
mechs = []
j = 0
print 'building NEURON simulation...'
for nrn in t.nrns:
    # get morphology
    print 'building ' + nrn.name + '...'
    cells.append(h.Section(cell=nrn.name))
    cells[j].nseg = 1
    print 'nseg:' + str(cells[j].nseg)
    cells[j].cm = nrn.cm # uF/cm2
    print 'cm:' +str(cells[j].cm)
    cells[j].diam = 1 # um
    print 'diam:'+ str(cells[j].diam)
    cells[j].L = 3.1831*10**7 # um, just make the cell be 1 cm**2
    # cells[j].L = nrn.am/np.pi*10**5 # um
    print 'L:' + str(cells[j].L)
    # total area = pi*diam*L
    
    # get mechanisms
    for chnl in nrn.chnls:
        if chnl.method == '5':
            print 'adding leak'
            cells[j].insert('pas')
            for seg in cells[j]:
                seg.pas.g = chnl.g*10**-6 # S/cm**2
                print 'g: ' + str(seg.pas.g)
                seg.pas.e = chnl.E # mV
                print 'e: ' + str(seg.pas.e)

        elif chnl.method == '3':
            print 'adding '+ chnl.name
            mechs.append(h.snnap_ionic3(cells[j](0.5)))
            mn = len(mechs) -1
            mechs[mn].e          =   chnl.E   # (mV)
            print 'e: ' + str(mechs[mn].e)
            mechs[mn].gmax       =   chnl.g   # (uS)
            print 'gmax: ' + str(mechs[mn].gmax)
            mechs[mn].p          =   chnl.P_Ivd
            print 'p: ' + str(mechs[mn].p)

            mechs[mn].hA         =   chnl.h_ssA   # (mV)
            print 'hA: ' + str(mechs[mn].hA)
            mechs[mn].sA         =   chnl.s_ssA   # (mV)
            print 'sA: ' + str(mechs[mn].sA)

            mechs[mn].tauAmin    =   chnl.tn_tA*10**3    # (ms)
            print 'tauAmin: ' + str(mechs[mn].tauAmin)
            mechs[mn].tauAmax    =   chnl.tx_tA*10**3    # (ms)
            print 'tauAmax: ' + str(mechs[mn].tauAmax)
            mechs[mn].htauA      =   -chnl.h_tA     # (mV)
            print 'htauA: ' + str(mechs[mn].htauA)
            mechs[mn].stauA      =   chnl.s_tA     # (mV)
            print 'stauA: ' + str(mechs[mn].stauA)

        elif chnl.method == '1':
            print 'adding '+ chnl.name
            mechs.append(h.snnap_ionic1(cells[j](0.5)))
            mn = len(mechs) -1
            mechs[mn].e          =   chnl.E   # (mV)
            print 'e: ' + str(mechs[mn].e)
            mechs[mn].gmax       =   chnl.g   # (uS)
            print 'gmax: ' + str(mechs[mn].gmax)
            mechs[mn].p          =   chnl.P_Ivd
            print 'p: ' + str(mechs[mn].p)

            mechs[mn].hA         =   chnl.h_ssA   # (mV)
            print 'hA: ' + str(mechs[mn].hA)
            mechs[mn].sA         =   chnl.s_ssA   # (mV)
            print 'sA: ' + str(mechs[mn].sA)

            mechs[mn].tauAmin    =   chnl.tn_tA*10**3    # (ms)
            print 'tauAmin: ' + str(mechs[mn].tauAmin)
            mechs[mn].tauAmax    =   chnl.tx_tA*10**3    # (ms)
            print 'tauAmax: ' + str(mechs[mn].tauAmax)
            mechs[mn].htauA      =   -chnl.h_tA     # (mV)
            print 'htauA: ' + str(mechs[mn].htauA)
            mechs[mn].stauA      =   chnl.s_tA     # (mV)
            print 'stauA: ' + str(mechs[mn].stauA)

            mechs[mn].hB         =   chnl.h_ssB   # (mV)
            print 'hB: ' + str(mechs[mn].hB)
            mechs[mn].sB         =   chnl.s_ssB   # (mV)
            print 'sB: ' + str(mechs[mn].sB)
            mechs[mn].pB         =   chnl.P_ssB   # (mV)
            print 'pB: ' + str(mechs[mn].pB)
            mechs[mn].Bmin         =   0   # (mV)
            print 'Bmin: ' + str(mechs[mn].Bmin)

            mechs[mn].tauBmin    =   chnl.tn_tB*10**3    # (ms)
            print 'tauBmin: ' + str(mechs[mn].tauBmin)
            mechs[mn].tauBmax    =   chnl.tx_tB*10**3    # (ms)
            print 'tauBmax: ' + str(mechs[mn].tauBmax)
            mechs[mn].htauB      =   chnl.h_tB     # (mV)
            print 'htauB: ' + str(mechs[mn].htauB)
            mechs[mn].stauB      =   chnl.s_tB     # (mV)
            print 'stauB: ' + str(mechs[mn].stauB)

        else:
            raise NotImplementedError
    print 'done building ' + nrn.name + '.'
    j+=1

for mech in mechs:
    print mech.has_loc()

# # current clamp
# i = h.IClamp(cells[0](0.5))
# i.delay = t.inj_start # ms
# i.dur = t.inj_stop-t.inj_start # ms
# i.amp = t.inj_mag*100 # nA
# # recording
time = h.Vector()
v = h.Vector()
time.record(h._ref_t)
v.record(cells[0](0.5)._ref_v)
# simulation
h.v_init = -70           # (mV)
h.tstop  = t.stop          # (ms) -- estimated from figure
h.cvode.active(1)      # enable variable time steps
h.finitialize()        # initialize state variables (INITIAL blocks)
h.fcurrent()           # initialize all currents    (BREAKPOINT blocks)
h.run()
# plotting
pyplot.plot(time, v)
pyplot.xlabel('time (ms)')
pyplot.ylabel('mV')
pyplot.show()