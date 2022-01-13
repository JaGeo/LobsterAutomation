import contextlib
import os

from pymatgen.analysis.bond_valence import BVAnalyzer
from pymatgen.analysis.chemenv.coordination_environments.chemenv_strategies import SimplestChemenvStrategy
from pymatgen.analysis.chemenv.coordination_environments.coordination_geometry_finder import LocalGeometryFinder
from pymatgen.analysis.chemenv.coordination_environments.structure_environments import LightStructureEnvironments
from pymatgen.core.structure import Structure

for directory in [
    "/hpc-user/jgeorge/PycharmProjects/Scripts_for_Automation/LobsterAutomation/Results/Yb14MnSb11/mp-568088/Spin_2/lobster_1",
    "/hpc-user/jgeorge/PycharmProjects/Scripts_for_Automation/LobsterAutomation/Results/Yb14MnSb11/mp-568088/Spin_mixed/lobster_1"]:

    for angle_cutoff in [0.3, 0.2]:

        # structure

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
            se = lgf.compute_structure_environments(only_cations=True, valences=valences)

            # compute light structure environments
            strategy = SimplestChemenvStrategy(distance_cutoff=1.4, angle_cutoff=angle_cutoff)
            lse = LightStructureEnvironments.from_structure_environments(strategy=strategy, structure_environments=se)

        print(directory.split("/")[-2])
        print("Angle Cutoff: " + str(angle_cutoff))
        for ienv, env in enumerate(lse.coordination_environments):
            if env is not None:
                print(str(struct[ienv].specie) + str(ienv + 1) + ': ' + str(env[0]["ce_symbol"]))
        print(" ")
