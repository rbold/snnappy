================================================================================
               - NEURON Reconstruction of Susswein et al. 2002 -
================================================================================

Susswein et al. 2002 present a conductance-based model of B63 and B31/B32,
interneurons found in the buccal ganglia of the marine mollusk Aplysia
californica and associated with grasper protraction during feeding motor
programs. Their model was originally implemented in SNNAP and is reimplemented
here in NEURON.


Created by:
   Jeffrey P Gill (jeff.gill@case.edu)
   Shang-Shen Yu

This project is available at:
   http://github.com/jpg18/sussweinetal2002/

Original model:
   Susswein AJ, Hurwitz I, Thorne R, Byrne JH, and Baxter DA. 2002.
   Mechanisms underlying fictive feeding in Aplysia: Coupling between a
   large neuron with plateau potentials activity and a spiking neuron.
   J Neurophysiol 87:2307-2323.

Usage:
   1. Compile the mod files by running mknrndll (Windows/Mac) or nrnivmodl
      (UNIX).
   2. Execute one of the "sim_*.hoc" files in NEURON to generate plots of the
      corresponding figure from Susswein et al. 2002.

Notes:
   The "create_*.hoc" files are subroutines used by the "sim_*.hoc" files and
   are not intended to be executed independently.

   Instances of the phrase "SNNAP code" found throughout these files refer to
   the original model implementation, generously provided to us by Dr. Douglas
   Baxter.

   The mod files provided here could be used to port other SNNAP models into
   NEURON (e.g., Ziv et al. 1994).
