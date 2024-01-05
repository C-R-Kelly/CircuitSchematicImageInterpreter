# Circuit Schematic Image Interpreter


**Author:** ***C. R. Kelly***   
**Email:** ***CK598@cam.ac.uk*** 


	
A configurable python package to segment a circuit diagram into its components, junctions and wires, identify the components using OCR, use this information to plot network graphs of the circuit and obtain & solve the fundamental matrices to obtain equations for voltages and currents at any point in the circuit.


To show how this package can be utilised, an example script has been included: [example scipt.py](/example_script.py)

To configure this package, all configuration parameters and their uses can be found in: [config.py](/CircuitSchematicImageInterpreter//config.py)
	
## Installation    
	 
	


Circuit Schematic Image Interpreter can be installed using pip.
	
`pip install git+https://github.com/C-R-Kelly/CircuitSchematicImageInterpreter`

	
	
     
## Usage  


### Images

**To import an image into the program and convert it into greyscale use:**
	
`image = io.importImage(path)`
	


**Various attributes of the image can then be pulled:**

`image.name` will return the file name.

`image.image` will return the greyscale converted image as a NumPy array.

`image.binaryImage` will return a binarised copy of the image.

`image.binarySkeleton`will return a binarised skeletonised copy of the image.

`image.centre, image.width, image.height` will return Returns the centroid of the image and the width & height in pixels.

`image.size` will return the size of the image in pixels.

`image.path` will return the file path of the image.
	
`image.getBorder()` will return the bounding box of the image.

**All display functions can be called directly off of each other. E.g., image.displayBinaryImage().plotComponents().plotWires().plotJunctions()**

`image.displayImage()` will plot the image in Matplotlib.

`image.displayBinaryImage()` will plot the binary image in matplotlib.

`image.displayBinarySkeleton()`	will plot the binarised skeletonised image in Matplotlib.

`image.plotComponents(Components, image)` will plot the ROIs on open image in matplotlib as a red bounding box + a red dot at the centroid.

`image.plotWires(HorizWires, VertWires)` will plot the horizontal and vertical wires on an image open in Matplotlib.

`image.plotJunctions(Junctions, Letters=True)` will plot the found junctions in matplotlib as a green dot. If `Letters=True`, a blue letter will also appear next to the junction. Letters go from A-Z.

`image.plotAll(Junctions, Components, HorizWires, VertWires, image)` will plot the image in matplotlib with all found junctions, components, horizontal wires and vertical wires. Returns NetworkX graph object.

	

### Wires
**To obtain the wires in the image use:**

`HorizWires, VertWires = actions.wireScanHough(image)` will return two lists containing all found horizontal and vertical wires respectively.
	


**Attributes of any wire in the list can then be pulled:**


`HorizWires[n].wire` will return a cropped segment of the binary image containing the wire.

`HorizWires[n].length` will return the length of the wire in pixels.

`HorizWires[n].centre` will return the centre coordinates of the wire.

`HorizWires[n].line` will return the coordinates of the start and end points of the wire as: `y1, y2, x1, x2`.

`HorizWires[n].start` will return the coordinates of the start point of the wire as: `y, x`.

`HorizWires[n].end` will return the coordinates of the end point of the wire as: `y, x`.

`HorizWires[n].getBorder()` will return the bounding box of the wire as: `top, bottom, left, right`.



### Components

**To obtain a list of found components in the image use:**
	
`Components = actions.objectDetection(HorizWires, VertWires)` will return a list of all found components in the image.

**Attributes of any component in the list can then be pulled:**

`Components[n].path` will return the path of the saved component image, if it has been exported.

`Components[n].id` will return the unique integer id of the component.

`Components[n].centroid` will return the centroid coordinates of the component as `y1, x1`.

`Components[n].centroidY, Components[n].centroidX` will return the `y` or `x` centroid coorindate of the component.

`Components[n].Height` will return the height of the bounding box of the component in pixels.

`Components[n].Width` will return the width of the bounding box of the component in pixels.

`Components[n].isVert` will return a boolean value of whether the component was found between two horizontal (False) or vertical (True) wires.

`Components[n].associatedHWires` If the component is horizontal, this returns a list of the two connecting horizontal wires.

`Components[n].associatedVWires` If the component is vertical, this returns a list of the two connecting vertical wires.

`Components[n].componentType` If OCR has been performed on all the components in the image, this returns a string of the component it was identified as.

`Components[n].unichar`	If OCR has been performed on all the components in the image, this returns the unichar of the component it was identified as.

`Components[n].terminalNo` If OCR has been performed on all the components in the image, this returns the number of terminals of the component it was identified as. If no OCR has been performed, this value defaults to `2`.

`Components[n].getRegion(image)` will return the bounding box of the component as `top, bottom, left, right`.



### Junctions
**To obtain a list of found junctions in the image use:**
	
`Junctions = actions.junctionDetection(HorizWires, VertWires)` will return a list of all found junctions in the image.


**Attributes of any junction in the list can then be pulled:**

`Junctions[n].id` will return the unique id of the junction which is a letter `A-Z`.

`Junctions[n].id_node` will return the unique id of the node the junction corresponds to which is a letter `A-Z`.

`Junctions[n].centroid`	will return the centroid coordinates of the junction as: `y1, x1`.

`Junctions[n].directions` If the junction is a tri junction, this will return a value of `N, S, E, or W` which correpsonds the direction the intersecting wire is going. North means the intersecting wire is vertical and the horizontal wire is at the top of said vertical wire.

`Junctions[n].type` will return the type of junction as `'Corner', 'Tri', or 'Quad'`.

`Junctions[n].associatedHWires` will return a list of all horizontal wires passing through or connecting to the junction.

`Junctions[n].associatedVWires` will return a list of all vertical wires passing through or connecting to the junction.

`Junctions[n].isNode` will return Returns a boolean value of whether the junction is a node or whether it merges to another node.

`Junctions[n].connectedNodesH` will return Returns a list of all other junctions that connect directly to this junction by a horizontal wire.

`Junctions[n].connectedNodesV` will return a list of all other junctions that connect directly to this junction by a vertical wire.



### OCR Component Identification
**To identify a list of found components using OCR, first the components must be exported as individual images. For this use:**

`io.exportComponent(image, Components)`

Then, the indivual component images can be put together to form a single component line and OCR can then be performed on this line. For this use:

`OCRComponents(components)` This will then assign all the relevant component parameters: `Components[n].componentType, .unichar, .terminalNo`.



### Network Graphs

**A network graph of the circuit can now be generated. To pull the NetworkX graph object use:**
	
`G = image.getNetworkGraph(Junctions, Components, draw=True)` If draw is set to True, the network graph will be plotted using Matplotlib.

**Other graphs can also be plotted using:**


`G.getCoTree(draw=True)` and `G.getSpanningTree(draw=True)`


**Graph attributes can then be pulled using:**
	
`G.componentList` will return the list of components used to form the graph edges.

`G.graph` will return the NetworkX graph object of the network graph.

`G.nodes` will return the list of nodes for the network graph.

`G.edges` will return the list of edges for the network graph.

`G.SP` will return the NetworkX graph object for the spanning tree of the graph.

`G.CH` will return the NetworkX graph object for the cotree of the graph.

`G.Bt` will return the reduced incidence matrix of the spanning tree.

`G.Bc` will return the reduced incidence matrix of the cotree.

`G.referenceVertexSP` will return the removed vertex of the incidence matrix for the spanning tree.

`G.referenceVertexCH` will return the removed vertex of the incidence matrix for the cotree.

`G.Df, G.Cf` If the fundamental cut-set and cycle matrices have been generated using.

`G.getFundamentalMatrices()` will return the fundamental matrices.

`G.getIMatrix(Graph, Reduced=True, returnRefVertex=False)` will return the incidence matrix of the graph object, Graph. If Reduced=True, the incidence matrix will be reduced. If returnRefVetex=True, it will return the vetex removed from the reduced incidence matrix.

`G.getSpanningTree(draw=False)` will return the spanning tree of the network graph. If `draw=True`, the spanning tree will be plotted using Matplotlib.

`G.getCoTree(draw=False)` will return the cotree of the network graph. If `draw=True`, the cotree will be plotted using Matplotlib.
	

**Warning: The following matricies rely on correct OCR, circuit segmentation, and a circuit where these matrices mathematically exist. Failure to meet these conditions may throw an error**

`G.getFundamentalMatrices()` will return the fundamental cut-set and cycle matrices, `Df` and `Cf`.

`G.linEquations()` will return the fundamental cut-set and cycle equations in matrix form.

`G.componentMatrix(components)` will return the component matrix accounting for components that have associated linear equations, the combined voltage/current column vector and the result column vector.
	
**Warning: If the `H` matrix is very large, finding the inverse of `H` to solve the matrix equation can take an extremely long time to calculate**

`G.getComponentEquations(matrices=False)` will return the solved matrix equation of `H^-1.y = x` where `H` is the component matrix, `y` is the result column vector and `x` is the voltage/current column vector. The return format is a matrix of the equation for each voltage and current value in the combined column vector. If `matrices=True`, matrices `H`, `x` and `y` are also returned.


**Notes: `G.Df` and `G.Cf` are not obtained automatically when a graph class instance is created as, if the fundamental matrices do not exist for your circuit / what is detected of your circuit then an error will be thrown. Thus these are obtained manually through `G.getFundamentalMatrices()`.**

**Currently, the only supported components for the component matrix are resistors, inductors and capacitors. Therefore, to make use of the solving of this matrix equation, the circuit can only contain these components + sources. Further, if OCR does not identify these components correctly, the matrix equation will likely fail and throw an error.**
	
		

### SPICE SIMULATION
	
	
**To create a SPICE netlist, use:**
	
`createNetList(image, components)` Saves a SPICE netlist that can be imported into software such as LTSpice. Saves as `<image_name>_netlist.txt` by default. File extension can be configured in [config.py](/CircuitSchematicImageInterpreter//config.py). Netlist uses nodes from network graph, so that must be generated first.
