import os

from atomate.vasp.powerups import add_additional_fields_to_taskdocs
from atomate.vasp.workflows.base.lobster import get_wf_lobster_test_basis
from fireworks import LaunchPad
from pymatgen.analysis.structure_matcher import StructureMatcher
from pymatgen.core.structure import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.symmetry.bandstructure import HighSymmKpath
from pymatgen.transformations.advanced_transformations import EnumerateStructureTransformation
from pymatgen.transformations.standard_transformations import SubstitutionTransformation
from pymatgen.transformations.advanced_transformations import CubicSupercellTransformation

dir_here = "Start_Structures"
directories = os.listdir(dir_here)

for iinput, input in enumerate(directories):
    print(input)

    struct = Structure.from_file(os.path.join(dir_here, input))

    spacegroup = SpacegroupAnalyzer(struct, symprec=0.1, angle_tolerance=10.0)
    struct = spacegroup.get_refined_structure()
    print(spacegroup.get_space_group_symbol())

    # This code will detect the subsitution matrix (Also works for N2O)
    min_el = None
    max_el = None
    for el in ["N", "O"]:
        print(struct.composition.element_composition[el])
        if abs(struct.composition.element_composition[el] - 2.0) < 1e-6:
            max_el = el
        if abs(struct.composition.element_composition[el] - 1.0) < 1e-6:
            min_el = el

    substitution_matrix = {min_el: {max_el: 1}}

    substitution_matrix2 = {max_el: {max_el: 2 / 3, min_el: 1 / 3}}

    name_str = input.split(".")[1]
    sub = SubstitutionTransformation(substitution_matrix)
    substituted = sub.apply_transformation(struct)
    sub2 = SubstitutionTransformation(substitution_matrix2)
    substituted2 = sub2.apply_transformation(substituted)

    # creates all relevant structural models
    trans = EnumerateStructureTransformation(max_cell_size=2)
    ss = trans.apply_transformation(substituted2, return_ranked_list=2000)

    list_structures = []
    for icell, cell in enumerate(ss):
        list_structures.append(cell["structure"])

    # searches for equivalent structures
    structurematcher = StructureMatcher(attempt_supercell=True, ltol=0.5, stol=0.5, angle_tol=13)
    sorted_structures = structurematcher.group_structures(list_structures)


    final_list_structures = []
    for icell, cell in enumerate(sorted_structures):
        # get primitive structure
        kpath = HighSymmKpath(cell[0], symprec=0.01)
        structure = kpath.prim
        transformation = CubicSupercellTransformation(min_length=16)
        structure=transformation.apply_transformation(structure=structure)

        final_list_structures.append(structure)

    os.makedirs("Substituted_structures_cubic_supercells/" + str(name_str))

    for icell, structure in enumerate(final_list_structures):
        # start workflow with this structure
        print(name_str + '_' + str(icell))
        print(structure)

        os.makedirs("Substituted_structures_cubic_supercells/" + str(name_str) + "/" + str(icell))
        structure.to(fmt="POSCAR",
                     filename="Substituted_structures_cubic_supercells/" + str(name_str) + "/" + str(icell) + "/POSCAR")
