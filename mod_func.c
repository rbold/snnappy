#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _snnap_ionic1_reg();
extern void _snnap_ionic3_reg();

void modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," snnap_ionic1.mod");
fprintf(stderr," snnap_ionic3.mod");
fprintf(stderr, "\n");
    }
_snnap_ionic1_reg();
_snnap_ionic3_reg();
}
