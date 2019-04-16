COMMENT
 * snnap_cs_nopsm.mod
 *
 * NEURON mechanism for implementing a SNNAP-style chemical synapse
 *
 * Copyright (c) 2012, Jeffrey P Gill and Shang-Shen Yu
 *
 * This file is part of NEURON Reconstruction of Susswein et al. 2002.
 * 
 * NEURON Reconstruction of Susswein et al. 2002 is free software: you can
 * redistribute it and/or modify it under the terms of the GNU General Public
 * License as published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version.
 * 
 * NEURON Reconstruction of Susswein et al. 2002 is distributed in the hope
 * that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
 * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with NEURON Reconstruction of Susswein et al. 2002.  If not, see
 * <http://www.gnu.org/licenses/>.
ENDCOMMENT


NEURON {
   : specify the interface to NEURON

   POINT_PROCESS
   : name of the mechanism

      snnap_cs_nopsm

   NONSPECIFIC_CURRENT
   : currents not associated with varying ion concentrations

      i

   RANGE
   : non-global variables and constants
   : specific to each instance of the mechanism

      i,
      e,
      g,

      on,
      dur,
      taucs,

      Acs,
      Bcs,
      SP
}

UNITS {
      (mV) = (millivolt)
      (uS) = (microsiemens)
      (nA) = (nanoamp)
}

PARAMETER {
   : declaration of fixed-value parameters

      e           (mV)
      g           (uS)

      dur         (ms)
      taucs       (ms)

      SP = 1
}

ASSIGNED {
   : declaration of non-state variables

      v           (mV)  : postsynaptic voltage
      i           (nA)
      on                : on=1 during a presynaptic spike
                        : on=0 in the absence of a presynaptic spike
}

STATE {
   : declaration of state variables

      Acs
      Bcs         (/ms) : first derivative of Acs
}

BREAKPOINT {
   : main computational block
   : set with fcurrent() and re-evaluated throughout the simulation
   : derivimplicit is used because the equations are not of the form y' = f(v,y)
   :    since they are nonlinear or involve states other than y
   : derivimplicit has first-order accuracy
   : equation A5
      SOLVE states METHOD derivimplicit
      i = g * Acs * (v - e)
}
INITIAL {
   : initial conditions
   : set with finitialize()
      on  = 0
      Acs = 0
      Bcs = 0
}
DERIVATIVE states {
   : differential equations for synaptic plasticity variables
   : equations A6, A8
      Acs' = Bcs
      Bcs' = BcsDeriv()
}

FUNCTION BcsDeriv() (/ms2) {
   : piecewise second-order differetial equation for Acs
   : depends on the state of the synapse
   : equations A6, A7

      if (on == 1) {
         BcsDeriv = (SP - 2 * taucs * Bcs - Acs) / taucs^2
      } else {
         BcsDeriv = (0  - 2 * taucs * Bcs - Acs) / taucs^2
      }
}

NET_RECEIVE (weight) {
   : receiver for NetCon events
   : external events triggered by a presynatic spike have flag=0
   : self-issued events triggered after a delay have flag=1
   : weight is not used

   if (flag == 0) {
      : presynaptic spike began
      if (!on) {
         on = 1            : turn the synapse on
         net_send(dur, 1)  : offset after dur with flag=1
      } else {
         net_move(t + dur) : already on, so postpone offset time
      }
   }

   if (flag == 1) {
      : presynaptic spike ended
      on = 0               : turn the synapse off
   }
}