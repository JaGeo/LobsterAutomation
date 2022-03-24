# LobsterAutomation
This is a package to reproduce the publication on Lobster automation ([ChemRxiv](https://doi.org/10.26434/chemrxiv-2022-2v424)). 

"Start_Scripts" includes two scripts to start all Lobster computations with
pymatgen, fireworks, and atomate.

You need to download the data from our second zenodo.org repository first.
You can get the data here: [https://doi.org/10.5281/zenodo.6373369](https://doi.org/10.5281/zenodo.6373369)

Please unzip the data and put it in the folder "LobsterAutomation".

You can then use the "Analysis_Scripts" to reproduce our publication.

- analyse_results_14_1_11.py will produce the automatic analysis for Yb14Mn1Sb11. 
- analyse_results_14_1_11_anion_anion.py will produce the automatic analysis including all bonds for Yb14Mn1Sb11
- analyse_14_1_11_chemenv.py will produce the geometric analysis of coordination environments with ChemEnv
- analyse_results_GaN.py will produce all plots and outputs for the GaN phases
- analyse_results_NaCl.py will produce all plots and outputs for the NaCl phases
- analyse_oxynitrides.py will produce all plots and outputs for the oxynitride systems

In "Analysis_Scripts/Outputs", you can find the outputs.


To produce the data, you can use the scripts in "Start_Scripts". 

- "start_workflows_bulk.py" will start all computations except for the oxynitride computations
- "start_defect_structures.py" will start the oxynitride computations


The following version numbers are needed for the workflows:
- pymatgen 2022.2.1
- atomate 1.0.3
- [enumlib 2.0.4](https://github.com/msg-byu/enumlib)


To analyze the results, you would need the latest version of:
- [LobsterPy](https://github.com/JaGeo/LobsterPy)
