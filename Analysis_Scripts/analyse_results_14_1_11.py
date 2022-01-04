import os

from lobsterpy.cohp.analyze import Analysis
from lobsterpy.cohp.describe import Description


for directory in [
    "/hpc-user/jgeorge/PycharmProjects/Scripts_for_Automation/LobsterAutomation/Results/Yb14MnSb11/mp-568088/Spin_1/lobster_1",
    "/hpc-user/jgeorge/PycharmProjects/Scripts_for_Automation/LobsterAutomation/Results/Yb14MnSb11/mp-568088/Spin_2/lobster_1",
    "/hpc-user/jgeorge/PycharmProjects/Scripts_for_Automation/LobsterAutomation/Results/Yb14MnSb11/mp-568088/Spin_mixed/lobster_1"]:
    # Setup analysis dict
    analyse = Analysis(path_to_poscar=os.path.join(directory, "POSCAR.gz"),
                       path_to_icohplist=os.path.join(directory, "ICOHPLIST.lobster.gz"),
                       path_to_cohpcar=os.path.join(directory, "COHPCAR.lobster.gz"),
                       path_to_charge=os.path.join(directory, "CHARGE.lobster.gz"), summed_spins=False)

    # Setup Desciption dict
    describe = Description(analysis_object=analyse)
    describe.write_description()

    # Automatic plots
    describe.plot_cohps(ylim=[-4, 2], xlim=[-4, 4], integrated=False)

    # different dicts that summarize the results
    print(analyse.condensed_bonding_analysis)
    print(analyse.final_dict_bonds)
    print(analyse.final_dict_cations)
