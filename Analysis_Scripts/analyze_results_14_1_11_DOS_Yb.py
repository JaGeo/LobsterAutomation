# Here, we will analyze the DOS of 14 1 11 for different basis sets
from pathlib import Path
#relevant classes
from pymatgen.io.lobster import Doscar
from pymatgen.electronic_structure.plotter import DosPlotter
from pymatgen.core.composition import Element

# elementwise density of states

for spin in ["Spin_2", "Spin_mixed"]:
    for lobster in ["lobster_0", "lobster_1"]:
        directory = (
            Path(__file__).parent.parent / f"Results/Yb14MnSb11/mp-568088/{spin}/{lobster}"
        )
        # read in DOSCAR.lobster
        doscar = Doscar(doscar=directory/"DOSCAR.lobster.gz", structure_file=directory/"POSCAR.gz")
        complete_dos = doscar.completedos
        # get structure object
        structure = complete_dos.structure
        Plotter = DosPlotter()
        el = Element("Yb")
        Plotter.add_dos_dict(complete_dos.get_element_spd_dos(el=el))
        Plotter.get_plot().show()

