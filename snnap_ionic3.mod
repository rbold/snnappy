COMMENT
 * snnap_ionic.mod
 *
 * NEURON mechanism for implementing a SNNAP-style ionic current
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

      snnap_ionic3

   NONSPECIFIC_CURRENT
   : currents not associated with varying ion concentrations

      i

   RANGE
   : non-global variables and constants
   : specific to each instance of the mechanism

      i,
      e,
      g,
      gmax,
      p,

      A,
      hA,
      sA,
      Ainit,
         
         

      tauAmin,
      tauAmax,
      htauA,
      stauA,
      ptauA,
      htauA2,
      stauA2,
      ptauA2
}

UNITS {
      (mV) = (millivolt)
      (uS) = (microsiemens)
      (nA) = (nanoamp)
}

PARAMETER {
   : declaration of fixed-value parameters

      e           (mV)
      gmax        (uS)
      p

      hA          (mV)
      sA          (mV)

      tauAmin     (ms)
      tauAmax     (ms)
      htauA       (mV)
      stauA       (mV)
      ptauA  = 1
      htauA2 = 0  (mV)
      stauA2 = 1  (mV)
      ptauA2 = 0

      Ainit
}

ASSIGNED {
   : declaration of non-state variables

      v           (mV)
      i           (nA)
      g           (uS)
}

STATE {
   : declaration of state variables

      A                 : activation
}

BREAKPOINT {
   : main computational block
   : set with fcurrent() and re-evaluated throughout the simulation
   : cnexp is used because the equations are of the form y' = f(v,y), are linear
   :    in y, and involve no other states
   : cnexp has second-order accuracy and is computationally efficient
   : equation A2

      SOLVE states METHOD cnexp

      g = gmax * A ^ p
      i = g * (v - e)
}

INITIAL {
   : initial conditions
   : set with finitialize()

      A = Ainf(v)
}

DERIVATIVE states {
   : differential equations for gating variables
   : equations A3a

      A' = (Ainf(v) - A) / tauA(v)
}

FUNCTION Ainf(v (mV)) () {
   : steady state value of activation variable
   : equation A4a

      Ainf = 1 / (1 + exp((hA - v)/sA))
}

FUNCTION tauA(v (mV)) (ms) {
   : time constant of activation variable (double exponential form)
   : equation A4c (see also Ziv et. al 1994, table 1)

      tauA = tauAmin + (tauAmax - tauAmin) / (1 + exp((v - htauA)/stauA))^ptauA / (1 + exp((v - htauA2)/stauA2))^ptauA2
}
