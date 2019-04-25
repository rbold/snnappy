# snnappy

Translate SNNAP simulations automatically with Python

## Usage

Convert example simulation to NEURON

1. Compile `*.mod` files 

    - [Windows](https://www.neuron.yale.edu/neuron/static/docs/nmodl/mswin.html)
    - [Mac](https://www.neuron.yale.edu/neuron/static/docs/nmodl/macos.html)
    - [Linux/Unix](https://www.neuron.yale.edu/neuron/static/docs/nmodl/unix.html)

2. Run `snnap2neuron.py`

`*.smu.ing` files are generated whenever a SNNAP simulation is run, to convert another simulation to NEURON:

1. Run it in SNNAP

2. Copy the resulting `*.smu.ing` file to the same directory as `snnap2neuron.py`, and change the variable `ing_file` in `snnap2neuron.py` to the relative location of the `*.smu.ing` file.

*However, note that not all SNNAP features have been implemented in this conversion method.*

When running `snnap2neuron.py`, two log files are generated. One lists the information extracted from the `*.smu.ing` file by `snnappy.py` in a slightly more readable format. It is named `*simulation name*_import.log`. The other details the process of building the NEURON simulation. It is named `*simulation name*_s2n.log`.

## Acknowledgements

The `*.mod` files are slightly modified versions of those written by Jeffery P. Gill and Shang-Shen Yu to be used in [their conversion of another SNNAP simulation](https://github.com/jpgill86/sussweinetal2002). Thay are used with permission.

---
Contact Reid Bolding (reid@case.edu) for more info.