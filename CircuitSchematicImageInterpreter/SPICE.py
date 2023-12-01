"""
SPICE Tools
===========

A set of tools for creating netlists for circuits and running basic simulations

author: C. R. Kelly
email: CK598@cam.ac.uk

"""
import os
from .config import SPICE_Config


def findGroundNode(components):
    # Finds ground nodes by identifying the second node of any present cell.
    # Replaces all occurrences of this node letter with '0' (SPICE syntax for ground)

    for component in components:
        if component.componentType == 'Cell':
            groundNode = component.nodes[1]
            for c in components:
                for counter, node in enumerate(c.nodes):
                    if node == groundNode:
                        if counter == 0:
                            c.nodes = (0, c.nodes[1])
                        else:
                            c.nodes = (c.nodes[0], 0)

    return components


def createNetList(image, components):
    # Import config
    config = SPICE_Config()

    Values = config.AssignDefaultComponentValues
    components = findGroundNode(components)

    # Component Counters
    resistors = 1
    capacitors = 1
    inductors = 1
    cells = 1

    #### file io
    output_path = os.path.splitext(image.path)[0] + '_netlist' + config.NetlistExtension  # output path
    netlist = open(output_path, 'w')  # open netlist file

    netlist.write('* ' + output_path)  # netlist title

    for component in components:

        if not Values:

            if component.componentType == 'Cell' or component.componentType == 'Source':
                netlist.write('\nV' + str(cells) + ' ' + str(component.nodes[0]) + ' ' + str(component.nodes[1]))
                cells += 1
            elif component.componentType == 'Resistor (US)' or component.componentType == 'Resistor (EU)':
                netlist.write('\nR' + str(resistors) + ' ' + str(component.nodes[0]) + ' ' + str(component.nodes[1]))
                resistors += 1
            elif component.componentType == 'Capacitor':
                netlist.write('\nC' + str(capacitors) + ' ' + str(component.nodes[0]) + ' ' + str(component.nodes[1]))
                capacitors += 1
            elif component.componentType == 'Inductor':
                netlist.write('\nL' + str(inductors) + ' ' + str(component.nodes[0]) + ' ' + str(component.nodes[1]))
                inductors += 1

        else:

            if component.componentType == 'Cell' or component.componentType == 'Source':
                netlist.write('\nV' + str(cells) + ' ' + str(component.nodes[0]) + ' ' + str(
                    component.nodes[1]) + ' ' + config.Cell)
                cells += 1
            elif component.componentType == 'Resistor (US)' or component.componentType == 'Resistor (EU)':
                netlist.write('\nR' + str(resistors) + ' ' + str(component.nodes[0]) + ' ' + str(
                    component.nodes[1]) + ' ' + config.Resistor)
                resistors += 1
            elif component.componentType == 'Capacitor':
                netlist.write('\nC' + str(capacitors) + ' ' + str(component.nodes[0]) + ' ' + str(
                    component.nodes[1]) + ' ' + config.Capacitor)
                capacitors += 1
            elif component.componentType == 'Inductor':
                netlist.write('\nL' + str(inductors) + ' ' + str(component.nodes[0]) + ' ' + str(
                    component.nodes[1]) + ' ' + config.Inductor)
                inductors += 1

    netlist.write('\n.tran 0.1s 1s 0s')
    netlist.write('\n.end')
    netlist.close()
