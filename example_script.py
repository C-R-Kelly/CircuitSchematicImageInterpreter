# -*- coding: utf-8 -*-
"""

author: C. R. Kelly
email: CK598@cam.ac.uk

"""
from CircuitSchematicImageInterpreter.SPICE import createNetList
from CircuitSchematicImageInterpreter.io import importImage, exportComponent
from CircuitSchematicImageInterpreter.actions import wireScanHough, objectDetection, junctionDetection
from CircuitSchematicImageInterpreter.ocr import OCRComponents

# Path to circuit image
PATH = 'Test Images/test_image.tif'

# Import image
image = importImage(PATH)

# Get Wires
HorizWires, VertWires = wireScanHough(image)

# Get Components
components = objectDetection(HorizWires, VertWires)

# Get Junctions
junctions = junctionDetection(HorizWires, VertWires)

#### NUMERICAL OUTPUT
print("Number of components: ", len(components))
print()

exportComponent(image,
                components)  # Exports all found components as separate images to configured path, this is required for tesseract to create component line for OCR

# Combine all exported component images, then perform OCR on the component line image
OCRComponents(components)

# Plot Output
image.plotAll(junctions, components, HorizWires, VertWires, image)

# Get Graph
G = image.getNetworkGraph(junctions, components, draw=True)
G.getCoTree(draw=True)
G.getSpanningTree(draw=True)

### Warning:
### The following functions may throw an error if the OCR has made a mistake, or the circuit was segmented incorrectly
###

# Get fundamental matrices (if possible to calculate)
# G.getFundamentalMatrices()

# Get fundamental equations (if possible to calculate)
# G.linEquations()

# Get unsolved matrix equation for components of the circuit
# G.componentMatrix(components)


# Solve component matrix equation for circuit values (if possible to calculate)
# Warning, if the H matrix is very large, the inverse of H can take an extremely long time to calculate
# G.getComponentEquations(components)

# Create SPICE Netlist
createNetList(image, components)

