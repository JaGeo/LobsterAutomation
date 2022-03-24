import contextlib
import os

from pymatgen.analysis.bond_valence import BVAnalyzer
from pymatgen.analysis.chemenv.coordination_environments.chemenv_strategies import (
    SimplestChemenvStrategy,
)
from pymatgen.analysis.chemenv.coordination_environments.coordination_geometry_finder import (
    LocalGeometryFinder,
)
from pymatgen.analysis.chemenv.coordination_environments.structure_environments import (
    LightStructureEnvironments,
)
from pymatgen.core.structure import Structure

# The computations have to be downloaded from zenodo.org as they too large for a github repository
current_path = os.getcwd()
directory_results = os.path.join(current_path, "../Results")

# First folder contains spin-polarized computation, second one the one without.


# First folder contains spin-polarized computation, second one the one without.
for directory in [
    os.path.join(directory_results, "Yb14MnSb11/mp-568088/Spin_2/lobster_1"),
    os.path.join(directory_results, "Yb14MnSb11/mp-568088/Spin_mixed/lobster_1"),
]:
    for angle_cutoff in [0.3, 0.2]:
        with contextlib.redirect_stdout(None):
            with contextlib.redirect_stderr(None):
                struct = Structure.from_file(os.path.join(directory, "POSCAR.gz"))

            # get valences with Bond Valence analyser
            ana = BVAnalyzer()
            valences = ana.get_valences(struct)
            # Setup the local geometry finder
            lgf = LocalGeometryFinder()

            lgf.setup_structure(structure=struct)
            # Get the StructureEnvironments
            se = lgf.compute_structure_environments(
                only_cations=True, valences=valences
            )

            # compute light structure environments
            strategy = SimplestChemenvStrategy(
                distance_cutoff=1.4, angle_cutoff=angle_cutoff
            )
            lse = LightStructureEnvironments.from_structure_environments(
                strategy=strategy, structure_environments=se
            )

        print(directory.split("/")[-2])
        print("Angle Cutoff: " + str(angle_cutoff))
        for ienv, env in enumerate(lse.coordination_environments):
            if env is not None:
                print(
                    str(struct[ienv].specie)
                    + str(ienv + 1)
                    + ": "
                    + str(env[0]["ce_symbol"])
                )
        print(" ")
