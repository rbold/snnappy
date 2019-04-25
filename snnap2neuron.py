'''
Using information describing a SNNAP simulation which is extracted from a .ing file by
snnappy.py to recreate results in NEURON

Change variable ing_file to try on other simulations.

This also outputs a log file describing each step in recreating the results for debugging purposes.

Written by Reid Bolding, contact reid@case.edu
'''

from neuron import h, gui # gui is optional
h.load_file('stdrun.hoc')
import matplotlib.pyplot as plt
import snnappy
import numpy as np
import sys

ssim = snnappy.snnapsim()
ing_file = 'INGfiles/CS_inh.smu.ing' # relative path to *.ing file to convert to NEURON
ssim.from_ing(ing_file)

print 'building NEURON simulation...'

old_stdout = sys.stdout
log_file = open(ssim.name+'_s2n.log','w')
sys.stdout = log_file

# create NEURON versions of SNNAP neurons
cells = []
mechs = []
Is = []
j = 0 # iterate index
print 'building NEURON simulation...'
print 'building neurons...'
for nrn in ssim.nrns:
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

            if chnl.tAmeth == '2':
                mechs[mn].tauAmin    =   chnl.tn_tA*10**3    # (ms)
                print 'tauAmin: ' + str(mechs[mn].tauAmin)
                mechs[mn].htauA      =   chnl.h_tA     # (mV)
                print 'htauA: ' + str(mechs[mn].htauA)
                mechs[mn].stauA      =   chnl.s_tA     # (mV)
                print 'stauA: ' + str(mechs[mn].stauA)
            elif chnl.tAmeth == '3':
                mechs[mn].tauAmin    =   chnl.tn_tA*10**3    # (ms)
                print 'tauAmin: ' + str(mechs[mn].tauAmin)
                mechs[mn].htauA      =   chnl.h_tA     # (mV)
                print 'htauA: ' + str(mechs[mn].htauA)
                mechs[mn].stauA      =   chnl.s_tA     # (mV)
                print 'stauA: ' + str(mechs[mn].stauA)
                mechs[mn].htauA2      =   chnl.h2_tA     # (mV)
                print 'htauA2: ' + str(mechs[mn].htauA2)
                mechs[mn].stauA2      =   chnl.s2_tA     # (mV)
                print 'stauA2: ' + str(mechs[mn].stauA2)
                mechs[mn].ptauA2      = chnl.P2_tA
                print 'ptauA2: ' + str(mechs[mn].ptauA2)

            mechs[mn].tauAmax    =   chnl.tx_tA*10**3    # (ms)
            print 'tauAmax: ' + str(mechs[mn].tauAmax)

            mechs[mn].Ainit = chnl.A_init
            print 'Ainit: ' + str(mechs[mn].Ainit)

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

            if chnl.tAmeth =='2':
                mechs[mn].tauAmin    =   chnl.tn_tA*10**3    # (ms)
                print 'tauAmin: ' + str(mechs[mn].tauAmin)
                mechs[mn].htauA      =   chnl.h_tA     # (mV)
                print 'htauA: ' + str(mechs[mn].htauA)
                mechs[mn].stauA      =   chnl.s_tA     # (mV)
                print 'stauA: ' + str(mechs[mn].stauA)
            elif chnl.tAmeth == '3':
                mechs[mn].tauAmin    =   chnl.tn_tA*10**3    # (ms)
                print 'tauAmin: ' + str(mechs[mn].tauAmin)
                mechs[mn].htauA      =   chnl.h_tA     # (mV)
                print 'htauA: ' + str(mechs[mn].htauA)
                mechs[mn].stauA      =   chnl.s_tA     # (mV)
                print 'stauA: ' + str(mechs[mn].stauA)
                mechs[mn].htauA2      =   chnl.h2_tA     # (mV)
                print 'htauA2: ' + str(mechs[mn].htauA2)
                mechs[mn].stauA2      =   chnl.s2_tA     # (mV)
                print 'stauA2: ' + str(mechs[mn].stauA2)
                mechs[mn].ptauA2      = chnl.P2_tA
                print 'ptauA2: ' + str(mechs[mn].ptauA2)
            mechs[mn].tauAmax    =   chnl.tx_tA*10**3    # (ms)
            print 'tauAmax: ' + str(mechs[mn].tauAmax)

            mechs[mn].hB         =   chnl.h_ssB   # (mV)
            print 'hB: ' + str(mechs[mn].hB)
            mechs[mn].sB         =   chnl.s_ssB   # (mV)
            print 'sB: ' + str(mechs[mn].sB)
            mechs[mn].pB         =   chnl.P_ssB   # (mV)
            print 'pB: ' + str(mechs[mn].pB)
            if chnl.ssBmeth == '1':
                mechs[mn].Bmin         =   0   # (mV)
            else:
                mechs[mn].Bmin         =   chnl.Bn   # (mV)
            print 'Bmin: ' + str(mechs[mn].Bmin)

            if chnl.tBmeth =='2':
                mechs[mn].tauBmin    =   chnl.tn_tB*10**3    # (ms)
                print 'tauBmin: ' + str(mechs[mn].tauBmin)
                mechs[mn].htauB      =   chnl.h_tB     # (mV)
                print 'htauB: ' + str(mechs[mn].htauB)
                mechs[mn].stauB      =   chnl.s_tB     # (mV)
                print 'stauB: ' + str(mechs[mn].stauB)
            mechs[mn].tauBmax    =   chnl.tx_tB*10**3    # (ms)
            print 'tauBmax: ' + str(mechs[mn].tauBmax)

            mechs[mn].Ainit = chnl.A_init
            print 'Ainit: ' + str(mechs[mn].Ainit)
            mechs[mn].Binit = chnl.B_init
            print 'Binit: ' + str(mechs[mn].Binit)

        else:
            raise NotImplementedError
    print 'done building ' + nrn.name + '.'
    j+=1

csyns = []
netcons = []
print 'building '+str(len(ssim.csyns))+'chemical synapses...'
for csyn in ssim.csyns:
        if csyn.method == '1':
            print 'adding chemical synapse from neuron ' + csyn.pre_name + ' to '+csyn.post_name
            if csyn.PSMmeth == '1':
                csyns.append(h.snnap_cs(cells[csyn.pre_num](0.5)))
                cn = len(csyns) -1
                csyns[cn].tauSP1          =   csyn.ud*1000 # ms
                print 'tauSP1: ' + str(csyns[cn].tauSP1)
                csyns[cn].tauSP2          =   csyn.ur*1000 # ms
                print 'tauSP2: ' + str(csyns[cn].tauSP2)
            else:
                csyns.append(h.snnap_cs_nopsm(cells[csyn.pre_num](0.5)))
                cn = len(csyns) -1
            csyns[cn].e          =   csyn.E   # (mV)
            print 'e: ' + str(csyns[cn].e)
            csyns[cn].g       =   csyn.g # uS
            print 'g: ' + str(csyns[cn].g)
            csyns[cn].dur          =   ssim.nrns[csyn.pre_num].spikdur # ms
            print 'dur: ' + str(csyns[cn].dur)
            csyns[cn].taucs          =   csyn.u*1000 # ms
            print 'taucs: ' + str(csyns[cn].taucs)
            netcons.append(h.NetCon(cells[csyn.post_num](0.5)._ref_v, csyns[cn],-10, 0, 1,sec=cells[csyn.post_num]))
        else:
            raise NotImplementedError

# create NEURON version of SNNAP electrical synapses, a LinearMechanism
print 'building electrical synapses as linearmechanism...'
ne   = len(ssim.nrns)       # size of matrix describing electrical synapses
c    = h.Matrix(ne,ne,2)   # sparse (unallocated) zero matrix (efficient)
g    = h.Matrix(ne,ne)
y    = h.Vector(ne)
R1   = h.Vector(ne) # add randomness by playing vector into variable, have not implemented
R2   = h.Vector(ne)
b    = h.Vector(ne)
sl   = h.SectionList()   # list of cells; order corresponds to y
xvec = h.Vector(ne, 0.5)  # locations of the synaptic connections
for cell in cells:
    sl.append(sec=cell)
for esyn in ssim.esyns:
    # Ies(1) = G1*(post-pre)
    g.x[esyn.pre_num][esyn.post_num] = -esyn.G1*10**-6 # S/cm**2
    g.x[esyn.pre_num][esyn.pre_num] = esyn.G1*10**-6 # S/cm**2
    # Ies(2) = G2*(pre-post)
    g.x[esyn.post_num][esyn.post_num] = esyn.G2*10**-6 # S/cm**2
    g.x[esyn.post_num][esyn.pre_num] = -esyn.G2*10**-6 # S/cm**2
es = h.LinearMechanism(c, g, y, b, sl, xvec)


# current clamps
j = 0 # iterate index
for cinj in ssim.cinjs:
    for nrn in ssim.nrns:
        if nrn.name == cinj.nrn_name:
            nrn_num = nrn.num
    Is.append(h.IClamp(cells[nrn_num](0.5))) 
    print 'injection to '+ cinj.nrn_name + ' ' +str(nrn_num)
    Is[j].delay = cinj.start # ms
    Is[j].dur = cinj.stop-cinj.start # ms
    Is[j].amp = cinj.mag # nA
    print 'amplitude '+ str(cinj.mag)
    j+=1
# recording
time = h.Vector()
time.record(h._ref_t)
vs = []
j = 0 # iterate index
for cell in cells:
    vs.append(h.Vector())
    vs[j].record(cells[j](0.5)._ref_v)
    j+=1

# custom initialization
h.tstop  = ssim.stop       # (ms)
h.cvode.active(1)      # enable variable time steps
j=0
for nrn in ssim.nrns:
    # trying to set unique initial voltage for each neuron here, it does not seem to work
    # I think a hoc helper file would help with some of these issues 
    cells[j].v = nrn.vminit
    print 'set '+str(cells[j])+' initial voltage to ' +str(nrn.vminit)
    j+=1
print('initializing...')
# only need the following if states have been changed
if h.cvode.active():
    h.cvode.re_init()
else:
    h.fcurrent()
h.frecord_init()
h.run()

sys.stdout = old_stdout
log_file.close()

# plotting
# order = [2,7,4,3,9,8,5,0,6,1] # plot membrane voltages in a certain order to match SNNAP figure
order = []
pltf = 2000
pltt = 15000
for j in range(len(vs)):
    plt.subplot(len(vs), 1, j+1)
    if order != []:
        ind = order[j]
    else:
        ind = j
    plt.plot(np.array(time)[pltf:pltt], np.array(vs[ind])[pltf:pltt],label=ssim.nrns[ind].name)
    plt.ylim(-72, 60)
    plt.legend(loc='right')
plt.xlabel('time (ms)')
plt.ylabel('mV')
plt.show()