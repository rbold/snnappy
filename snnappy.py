## This file contains classes representing SNNAP objects in python
import sys


class snnapsim:
    def from_ing(self, ing_file):
        print 'importing SNNAP simulation...'
        ing = open(ing_file, 'r').readlines() # list of lines as strings
        i = 0 # line index
        while i < len(ing):
            line = ing[i].split()
            if len(line) == 0:
                i += 1
            else:
                v = line[0]
                if v == "LOGICAL_NAME":
                    # load name
                    self.name = line[1]
                    old_stdout = sys.stdout
                    log_file = open(self.name+"_import.log","w")
                    sys.stdout = log_file
                    print "loading " + self.name +"..."
                    i += 1
                elif v == 'TIMING:':
                    # load times
                    self.start = float(line[1])*1000.0 # milliseconds
                    self.stop = float(line[2])*1000.0 # milliseconds
                    self.step = float(line[3])*1000.0 # milliseconds
                    print 'run from ' + str(self.start) + 'ms to ' + str(self.stop) +'ms'
                    print 'in steps of ' + str(self.step) + 'ms'
                    i += 1
                # skipping some stuff I won't need
                elif v == '#NEUR':
                    print line[1] + " neurons to load"
                    nrnct = int(line[1]) # number of neurons
                    i = self.getnrns(ing, nrnct, i+1)
                elif v == '#ESYN':
                    print line[1] + " electrical synapses to load"
                    i = self.getesyn(ing,int(line[1]),i+1)
                elif v == '#CSYN':
                    print line[1] + " chemical synapses to load"
                    i = self.getcsyn(ing, int(line[1]), i+1)
                    i += 1
                elif v == '#CINJ':
                    num_cinj = line[1]
                    print num_cinj + " current injection"
                    self.cinjs = []
                    if num_cinj != '0':
                        cinj_loaded = 0
                        while cinj_loaded < int(num_cinj):
                            i += 1
                            line = ing[i].split()
                            self.cinjs.append(snnapcinj())
                            self.cinjs[cinj_loaded].from_ing(line)
                            cinj_loaded += 1
                    else:
                        i+=1
                # skipping stuff again
                else:
                    i += 1
        print 'done loading ' + self.name + ' at line '+ str(i)
        sys.stdout = old_stdout
        log_file.close()
    
    def getnrns(self, ing, n, i):
        self.nrns = []
        fn = 0 # number of neurons found
        while fn < n:
            line = ing[i].split()
            if len(line) == 0:
                i += 1
            else:
                if line[0] == 'neur#='+str(fn):
                    self.nrns.append(snnapnrn())
                    cn = len(self.nrns) -1
                    i =  self.nrns[cn].from_ing(cn, line[1], ing, i)
                    fn += 1
                else:
                    return i
        print 'done loading neurons at line '+ str(i)
        return i

    def getesyn(self, ing, n, i):
        self.esyns = []
        fn = 0 # number of neurons found
        while fn < n:
            line = ing[i].split()
            if len(line) == 0:
                i += 1
            else:
                if line[0] == 'esyn#='+str(fn):
                    self.esyns.append(snnapesyn())
                    cn = len(self.esyns) -1
                    i =  self.esyns[cn].from_ing(cn, ing, i)
                    fn += 1
                else:
                    return i
        print 'done loading electrical synapses at line '+ str(i)
        return i

    def getcsyn(self, ing, n, i):
        self.csyns = []
        fn = 0 # number of chemical synapses found
        while fn < n:
            line = ing[i].split()
            if len(line) == 0:
                i += 1
            else:
                if line[0] == 'csyn#='+str(fn):
                    self.csyns.append(snnapcsyn())
                    cn = len(self.csyns) -1
                    i =  self.csyns[cn].from_ing(cn, ing, i)-1
                    fn += 1
                else:
                    return i
        print 'done loading chemical synapses at line '+ str(i)
        return i


class snnapnrn:
    def from_ing(self, num, name, ing, i):
        self.num = num
        self.name = name
        print 'loading neuron ' + self.name + '...'
        v = ''
        i += 1
        while v != '#TRP' and v != 'neur#='+str(num+1):
            line = ing[i].split()
            if len(line) == 0:
                i += 1
            else:
                v = line[0]
                if v == "THRESHOLD":
                    # load threshold
                    self.thresh = float(line[1]) # mV
                    i += 1
                elif v == 'SPIKDUR':
                    # load spike time
                    self.spikdur = float(line[1])*1000.0 # milliseconds
                    i += 1
                elif v == 'VMINIT':
                    # load init membrane voltage
                    self.vminit = float(line[1]) # mV
                    i += 1
                elif v == 'CM':
                    # load membrane capacitance
                    self.cm = float(line[1]) # uF
                    i += 1
                elif v == 'MEM_AREA':
                    # load membrane area
                    self.am = float(line[1]) # um**2
                    i += 1
                # skipping some stuff I won't need
                elif v == '#VDG':
                    print line[1] + " channels to load"
                    chnlct = int(line[1]) # number of channels
                    i = self.getchnls(ing, chnlct, i+1)
                else:
                    i += 1
        print 'done loading ' + self.name + ' at line '+ str(i)
        return i

    def getchnls(self, ing, n, i):
        self.chnls = []
        fn = 0 # number of channels found
        while fn < n:
            line = ing[i].split()
            if len(line) == 0:
                i += 1
            else:
                if line[0] == 'vdg#='+str(fn):
                    self.chnls.append(snnapchnl())
                    cn = len(self.chnls) -1
                    i =  self.chnls[cn].from_ing(cn, line[1], ing, i) - 1
                    fn += 1
                else:
                    i += 1
        print 'done loading channels at line '+ str(i)
        return i

class snnapchnl:
    def from_ing(self, num, name, ing, i):
        self.num = num
        self.name = name
        print 'loading channel ' + self.name + '...'
        v = ''
        i += 1
        while v != '#ION' and v != 'vdg#='+str(num+1):
            line = ing[i].split()
            if len(line) == 0:
                i += 1
            else:
                v = line[0]
                if v == 'Ivd':
                    i = self.getivd(line[1], ing, i)
                else:
                    i += 1
        print 'done loading ' + self.name + ' at line '+ str(i)
        return i
    
    def getivd(self, method, ing, i):
        # note this excludes a lot of features right now including randomness, R
        self.method = method
        if method == '1': 
            # First, get Ivd params
            i = i+2
            line = ing[i].split()
            self.g = float(line[0]) # uS or S/cm2 if using area
            self.P_Ivd = float(line[1])
            self.E = float(line[2]) # mV
            # Get A
            i = i+7
            line = ing[i].split()
            Ameth = line[1]
            i = self.getA(ing, i, Ameth)
            # Get B
            i = i+2
            line = ing[i].split()
            Bmeth = line[1]
            i = self.getB(ing, i, Bmeth)
            # Equations are:
            self.Ivd_equation = 'Ivd = G*(V -'+str(self.E)+')* fBR'
            self.G_equation = 'G = '+str(self.g)+' * A**'+str(self.P_Ivd)+' * B'
        elif method == '3':
            # First, get Ivd params
            i = i+2
            line = ing[i].split()
            self.g = float(line[0]) # uS or S/cm2 if using area
            self.P_Ivd = float(line[1])
            self.E = float(line[2]) # mV
            # Get A
            i = i+7
            line = ing[i].split()
            Ameth = line[1]
            i = self.getA(ing, i, Ameth)
            # Equations are:
            self.Ivd_equation = 'Ivd = G*(V -'+str(self.E)+')* fBR'
            self.G_equation = 'G = '+str(self.g)+' * A**'+str(self.P_Ivd)
        elif method == '5':
            # Get Ivd params
            i = i+2
            line = ing[i].split()
            self.g = float(line[0]) # uS or S/cm2 if using area
            self.E = float(line[1]) # mV
            # Equations are:
            self.Ivd_equation = 'Ivd = G*(V -'+str(self.E)+')* fBR'
            self.G_equation = 'G = '+str(self.g)
        else:
            print 'Ivd method ' + method + ' conversion not implemented'
        print self.Ivd_equation
        print self.G_equation
        return i
    
    def getA(self,ing,i,method):
        if method == '1':
                raise NotImplementedError
        elif method == '2':
            # dA/dt = (ssA-A)/tA
            i = i+2
            line = ing[i]
            self.A_init = float(line) # unitless
            # find ssA
            i = i+1
            line = ing[i].split()
            ssAmeth = line[1]
            i = self.getssA(ing, i, ssAmeth)
            # find tA
            i = i+1
            line = ing[i].split()
            tAmeth = line[1]
            i = self.gettA(ing, i, tAmeth)
            self.A_equation = 'dA/dt = (ssA-A)/tA, A_init='+str(self.A_init)
            print self.A_equation
        else:
            raise NotImplementedError
        return i

    def getssA(self,ing,i,method):
        if method == '1':
            i = i+2
            line = ing[i].split()
            self.h_ssA = float(line[0]) # mV
            self.s_ssA = float(line[1]) # mV
            self.P_ssA = float(line[2])
            self.ssA_equation = 'ssA = (1+e**(('+str(self.h_ssA)+'-V)/'+str(self.s_ssA)+')**-'+str(self.P_ssA)
            print self.ssA_equation
        else:
            raise NotImplementedError
        return i
    
    def gettA(self,ing,i,method):
        if method == '1':
            i = i+2
            line = ing[i].split()
            self.tx_tA = float(line[0]) # seconds
            self.tA_equation = 'tA = '+str(self.tx_tA)
            self.tAmeth = '1'
        elif method == '2':
            i = i+2
            line = ing[i].split()
            self.tx_tA = float(line[0]) # seconds
            self.tn_tA = float(line[1]) # seconds
            self.h_tA = float(line[2]) # mV
            self.s_tA = float(line[3]) # mV
            self.P_tA = float(line[4])
            self.tA_equation = 'tA = ('+str(self.tx_tA)+'-'+str(self.tn_tA)+\
                ')*(1+e**((V-'+str(self.h_tA)+')/'+str(self.s_tA)+'))**-'+str(self.P_tA)\
                    +' + '+str(self.tn_tA)
            print self.tA_equation
            self.tAmeth = '2'
        elif method == '3':
            i = i+2
            line = ing[i].split()
            self.tx_tA = float(line[0]) # seconds
            self.tn_tA = float(line[1]) # seconds
            self.h_tA = float(line[2]) # mV
            self.s_tA = float(line[3]) # mV
            self.P_tA = float(line[4])
            self.h2_tA = float(line[5]) # mV
            self.s2_tA = float(line[6]) # mV
            self.P2_tA = float(line[7])
            self.tA_equation = 'tA = ('+str(self.tx_tA)+'-'+str(self.tn_tA)+\
                ')*(1+e**((V-'+str(self.h_tA)+')/'+str(self.s_tA)+'))**-'+str(self.P_tA)\
                    +'*(1+e**((V-'+str(self.h2_tA)+')/'+str(self.s2_tA)+'))**-'+str(self.P2_tA)\
                    +' + '+str(self.tn_tA)
            print self.tA_equation
            self.tAmeth = '3'
        else:
            raise NotImplementedError
        return i
    
    def getB(self,ing,i,method):
        if method == '1':
                raise NotImplementedError
        elif method == '2':
            i = i+2
            line = ing[i]
            self.B_init = float(line) # unitless
            # find ssB
            i = i+1
            line = ing[i].split()
            ssBmeth = line[1]
            i = self.getssB(ing, i, ssBmeth)
            # find tB
            i = i+1
            line = ing[i].split()
            tBmeth = line[1]
            i = self.gettB(ing, i, tBmeth)
            self.B_equation = 'dB/dt = (ssB-B)/tB, B_init='+str(self.B_init)
            print self.B_equation
        else:
            raise NotImplementedError
        return i


    def getssB(self,ing,i,method):
        self.ssBmeth = method
        if method == '1':
            i = i+2
            line = ing[i].split()
            self.h_ssB = float(line[0]) # mV
            self.s_ssB = float(line[1]) # mV
            self.P_ssB = float(line[2])
            self.ssB_equation = 'ssB = (1+e**((V-'+str(self.h_ssB)+')/'+str(self.s_ssB)+')**-'+str(self.P_ssB)
            print self.ssB_equation
        elif method == '2':
            i = i+2
            line = ing[i].split()
            self.h_ssB = float(line[1]) # mV
            self.s_ssB = float(line[2]) # mV
            self.P_ssB = float(line[3])
            self.Bn = float(line[0]) # mV
            self.ssB_equation = 'ssB = '+str(self.Bn)+'+(1-'+str(self.Bn)+')*(1+e**((V-'+str(self.h_ssB)+')/'+str(self.s_ssB)+')**-'+str(self.P_ssB)
            print self.ssB_equation
        else:
            raise NotImplementedError
        return i
    
    def gettB(self,ing,i,method):
        self.tBmeth = method
        if method == '1':
            i = i+2
            line = ing[i].split()
            self.tx_tB = float(line[0]) # seconds
            self.tB_equation = 'tB = '+str(self.tx_tB)
        elif method == '2':
            i = i+2
            line = ing[i].split()
            self.tx_tB = float(line[0]) # seconds
            self.tn_tB = float(line[1]) # seconds
            self.h_tB = float(line[2]) # mV
            self.s_tB = float(line[3]) # mV
            self.P_tB = float(line[4])
            self.tB_equation = 'tB = ('+str(self.tx_tB)+'-'+str(self.tn_tB)+')*(1+e**((V-'+str(self.h_tB)+')/'+str(self.s_tB)+'))**-'+str(self.P_tB)+' + '+str(self.tn_tB)
            print self.tB_equation
        else:
            raise NotImplementedError
        return i 

class snnapesyn:
    def from_ing(self, num, ing, i):
        self.num = num
        print 'loading electrical synapse ' + str(num)+ '...'
        line = ing[i].split()        
        self.pre_num = int(line[1])
        self.pre_name = line[2]
        print 'from neuron num: '+ line[1] + ' name: ' + line[2]
        self.post_num = int(line[3])
        self.post_name = line[4]
        print 'to neuron num: '+ line[3] + ' name: ' + line[4]
        v = ''
        i += 1
        while v != '#CSYN' and v != 'esyn#='+str(num+1):
            line = ing[i].split()
            if len(line) == 0:
                i += 1
            else:
                v = line[0]
                if v == 'Ies':
                    i = self.geties(line[1], ing, i)
                else:
                    i += 1
        print 'done loading electrical synapse ' + str(num) + ' at line '+ str(i)
        return i

    def geties(self, method, ing, i):
        # ignores random stuff
        self.method = method
        if method == '1': 
            # First, get Ies params
            i = i+2
            line = ing[i].split()
            self.G1 = float(line[0])
            self.G2 = float(line[1])
            # Equations are:
            self.Ies_equation1 = 'Ies(1) = '+line[0]+'*(V1-V2)'
            self.Ies_equation2 = 'Ies(2) = '+line[1]+'*(V2-V1)'
        else:
            raise NotImplementedError
        print self.Ies_equation1
        print self.Ies_equation2
        return i

class snnapcsyn:
    def from_ing(self, num, ing, i):
        self.num = num
        print 'loading chemical synapse ' + str(num)+ '...'
        line = ing[i].split()        
        self.pre_num = int(line[1])
        self.pre_name = line[2]
        print 'from neuron num: '+ line[1] + ' name: ' + line[2]
        self.post_num = int(line[3])
        self.post_name = line[4]
        print 'to neuron num: '+ line[3] + ' name: ' + line[4]
        v = ''
        i += 1
        while v != '#MSYN' and v != 'csyn#='+str(num+1):
            line = ing[i].split()
            if len(line) == 0:
                i += 1
            else:
                v = line[0]
                if v == 'Ics':
                    i = self.getics(line[1], ing, i)
                else:
                    i += 1
        print 'done loading chemical synapse ' + str(num) + ' at line '+ str(i)
        return i

    def getics(self, method, ing, i):
        # ignores random stuff
        self.method = method
        if method == '1': 
            # First, get Ics params
            i = i+2
            line = ing[i].split()
            self.g = float(line[0])
            self.E = float(line[1])
            # Get fAt
            i = i+4
            line = ing[i].split()
            fAtmeth = line[1]
            i = self.getfAt(ing, i, fAtmeth)
            # Equations are:
            self.Ics_equation = 'Ics = G*(V - '+str(self.E)+')'
            self.G_equation = 'G = '+str(self.g)+'*fAt'
        else:
            raise NotImplementedError
        print self.Ics_equation
        print self.G_equation
        return i
    
    def getfAt(self, ing, i, method):
        if method == '1':
            # Get At
            i = i+3
            line = ing[i].split()
            Atmeth = line[1]
            i = self.getAt(ing, i, Atmeth)
            self.fAt_equation = 'fAt = At'
            print self.fAt_equation
        else:
            raise NotImplementedError
        return i
    
    def getAt(self, ing, i, method):
        if method == '3':
            i += 1
            line = ing[i].split()
            self.is_Xt = int(line[1])
            i += 2
            line = ing[i].split()
            self.u = float(line[0])
            # Get Xt
            i += 1
            line = ing[i].split()
            Xtmeth = line[1]
            i = self.getXt(ing, i, Xtmeth)
            self.At_equation = '(d**2 At)/dt**2 = (Xt-2*'+str(self.u)+'*dAt/dt -At)/'+str(self.u)+'**2'
            print self.At_equation
        else:
            raise NotImplementedError
        return i

    def getXt(self, ing, i, method):
        if method == '1':
            i += 1
            line = ing[i].split()
            self.is_PSM = int(line[1])
            self.PSMmeth = '0'
            # no PSM for method 1
            self.Xt_equation = 'Xt = 1 when pre spiking, 0 when not'
            print self.Xt_equation
            i += 6
        elif method == '3':
            i += 1
            line = ing[i].split()
            self.is_PSM = int(line[1])
            # Get PSM
            i += 3
            line = ing[i].split()
            self.PSMmeth = line[1]
            i = self.getPSM(ing, i, self.PSMmeth)
            self.Xt_equation = 'Xt = PSM when pre spiking, 0 when not'
            print self.Xt_equation
            i += 1
        else:
            raise NotImplementedError
        return i

    def getPSM(self, ing, i, method):
        if method == '1':
            i += 2
            line = ing[i].split()
            self.ud = float(line[0])
            self.ur = float(line[1])
            self.psm_equation = 'dPSM/dt = -PSM/'+str(self.ud)+' when pre spiking, (1-PSM)/'+str(self.ur)+' when not'
            print self.psm_equation
        return i

    
class snnapcinj:
    def from_ing(self,line):
        self.num = int(line[0])
        self.nrn_name = line[1]
        print 'current injection to ' + line[1]
        self.start = float(line[2])*1000.0 # milliseconds
        print 'start at ' + line[2] + ' ms'
        self.stop = float(line[3])*1000.0 # milliseconds
        print 'stop at ' + line[3] + ' ms'                    
        self.mag = float(line[4]) # could be a function though
        print 'amplitude of ' + line[4] + ' nA'


