## This file contains classes representing SNNAP objects in python

class snnapsim:

    def from_ing(self, ing_file):
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
                    print "loading " + self.name +"..."
                    i += 1
                elif v == 'TIMING:':
                    # load times
                    self.start = line[1]
                    self.stop = line[2]
                    self.step = line[3]
                    print 'run from ' + self.start + 's to ' + self.stop +'s'
                    print 'in steps of ' + self.step + 's'
                    i += 1
                # skipping some stuff I won't need
                elif v == '#NEUR':
                    print line[1] + " neurons to load"
                    nrnct = int(line[1]) # number of neurons
                    i = self.getnrns(ing, nrnct, i+1)
                else:
                    i += 1
        print 'done loading ' + self.name + ' at line '+ str(i)
    
    def getnrns(self, ing, n, i):
        self.nrns = []
        for j in range(n):
            self.nrns.append(snnapnrn())
        fn = 0 # number of neurons found
        while fn < n:
            line = ing[i].split()
            if len(line) == 0:
                i += 1
            else:
                if line[0] == 'neur#='+str(fn):
                    i = self.nrns[fn].from_ing(fn, line[1], ing, i)
                    fn += 1
                else:
                    return i
        print 'done loading neurons at line '+ str(i)
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
                    self.thresh = line[1]
                    i += 1
                elif v == 'SPIKDUR':
                    # load spike time
                    self.spikdur = line[1]
                    i += 1
                elif v == 'VMINIT':
                    # load init membrane voltage
                    self.vminit = line[1]
                    i += 1
                elif v == 'CM':
                    # load membrane capacitance
                    self.cm = line[1]
                    i += 1
                elif v == 'MEM_AREA':
                    # load membrane area
                    self.spikdur = line[1]
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
        for j in range(n):
            self.chnls.append(snnapchnl())
        fn = 0 # number of channels found
        while fn < n:
            line = ing[i].split()
            if len(line) == 0:
                i += 1
            else:
                if line[0] == 'vdg#='+str(fn):
                    i = self.chnls[fn].from_ing(fn, line[1], ing, i) - 1
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
            v = line[0]
            if v == 'Ivd':
                i = self.getivd(line[1], ing, i)
            else:
                i += 1
        print 'done loading ' + self.name + ' at line '+ str(i)
        return i
    
    def getivd(self, method, ing, i):
        # note this excludes a lot of features right now including randomness, R
        if method == '1': 
            # First, get Ivd params
            i = i+2
            line = ing[i].split()
            self.g = line[0] # uS or S/cm2 if using area
            self.P_Ivd = line[1]
            self.E = line[2] # mV
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
            self.g = line[0] # uS or S/cm2 if using area
            self.P_Ivd = line[1]
            self.E = line[2] # mV
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
            self.g = line[0] # uS or S/cm2 if using area
            self.E = line[1] # mV
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
            self.A_init = line # unitless
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
            self.h_ssA = line[0] # mV
            self.s_ssA = line[1] # mV
            self.P_ssA = line[2]
            self.ssA_equation = 'ssA = (1+e**(('+str(self.h_ssA)+'-V)/'+str(self.s_ssA)+')**-'+str(self.P_ssA)
            print self.ssA_equation
        else:
            raise NotImplementedError
        return i
    
    def gettA(self,ing,i,method):
        if method == '2':
            i = i+2
            line = ing[i].split()
            self.tx_tA = line[0] # seconds
            self.tn_tA = line[1] # seconds
            self.h_tA = line[2] # mV
            self.s_tA = line[3] # mV
            self.P_tA = line[4]
            self.tA_equation = 'tA = ('+str(self.tx_tA)+'-'+str(self.tn_tA)+')*(1+e**((V-'+str(self.h_tA)+')/'+str(self.s_tA)+'))**-'+str(self.P_tA)+' + '+str(self.tn_tA)
            print self.tA_equation
        else:
            raise NotImplementedError
        return i
    
    def getB(self,ing,i,method):
        if method == '1':
                raise NotImplementedError
        elif method == '2':
            i = i+2
            line = ing[i]
            self.B_init = line # unitless
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
        if method == '1':
            i = i+2
            line = ing[i].split()
            self.h_ssB = line[0] # mV
            self.s_ssB = line[1] # mV
            self.P_ssB = line[2]
            self.ssB_equation = 'ssB = (1+e**(('+str(self.h_ssB)+'-V)/'+str(self.s_ssB)+')**-'+str(self.P_ssB)
            print self.ssB_equation
        else:
            raise NotImplementedError
        return i
    
    def gettB(self,ing,i,method):
        if method == '2':
            i = i+2
            line = ing[i].split()
            self.tx_tB = line[0] # seconds
            self.tn_tB = line[1] # seconds
            self.h_tB = line[2] # mV
            self.s_tB = line[3] # mV
            self.P_tB = line[4]
            self.tB_equation = 'tB = ('+str(self.tx_tB)+'-'+str(self.tn_tB)+')*(1+e**((V-'+str(self.h_tB)+')/'+str(self.s_tB)+'))**-'+str(self.P_tB)+' + '+str(self.tn_tB)
            print self.tB_equation
        else:
            raise NotImplementedError
        return i 
t = snnapsim()
t.from_ing("generic_cell_01.smu.ing")