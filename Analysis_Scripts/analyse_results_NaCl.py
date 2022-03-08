import os

from lobsterpy.cohp.analyze import Analysis
from lobsterpy.cohp.describe import Description

for directory in [
    "../Results/NaCl/mp-22862/Spin_1/lobster_0",
    "../Results/NaCl/mp-22851/Spin_1/lobster_0"]:
    # Setup analysis dict
    analyse = Analysis(path_to_poscar=os.path.join(directory, "POSCAR.gz"),
                       path_to_icohplist=os.path.join(directory, "ICOHPLIST.lobster.gz"),
                       path_to_cohpcar=os.path.join(directory, "COHPCAR.lobster.gz"),
                       path_to_charge=os.path.join(directory, "CHARGE.lobster.gz"),
                       path_to_madelung=os.path.join(directory, "MadelungEnergies.lobster.gz"),
                       whichbonds="cation-anion"
                       )

    # Setup Desciption dict
    describe = Description(analysis_object=analyse)
    describe.write_description()

    # Automatic plots
    describe.plot_cohps(ylim=[-4, 2], xlim=[-4, 4], integrated=False)

    # different dicts that summarize the results
    print(analyse.condensed_bonding_analysis)
    print(analyse.final_dict_bonds)
    print(analyse.final_dict_ions)
