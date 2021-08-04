# -*- coding: utf-8 -*-
"""
All Classes
===========

This set of classes contains all classes used in the package.

author: C. R. Kelly
email: CK598@cam.ac.uk

"""
from sympy import nsimplify
from sympy.matrices import Matrix
import matplotlib.pyplot as plt
from matplotlib import cm
import networkx as nx
import numpy as np
import math
import os

from .networkX import getNodes, getEdges, removeRedundantNodes
from .utils import binaryConversion, binarySkeleton
from .config import Config

config = Config()


# Circuit Diagram Image Class
class Image:

    def __init__(self, image, path):
        self.name = os.path.splitext(os.path.split(path)[1])[0]
        self.image = image
        self.binaryImage = binaryConversion(self.image)
        self.binarySkeleton = binarySkeleton(self.image)
        self.width = image.shape[1]
        self.height = image.shape[0]
        self.center = (int(self.width / 2), int(self.height / 2))
        self.size = np.size(image)
        self.path = path

    # gets image border
    def getBorder(self):
        rows = np.any(self.image, axis=0)
        columns = np.any(self.image, axis=1)
        left, right = np.where(rows)[0][[0, -1]]
        top, bottom = np.where(columns)[0][[0, -1]]
        imageBorder = [top, bottom, left, right]
        return imageBorder

    # Displays image
    def displayImage(self):
        plt.clf()
        plt.imshow(self.image, cmap=cm.gray)
        return self

    # Displays threshold image
    def displayBinaryImage(self):
        plt.clf()
        plt.imshow(self.binaryImage, cmap=cm.gray)
        return self

    # Displays threshold skeleton image
    def displayBinarySkeleton(self):
        plt.clf()
        plt.imshow(binarySkeleton(self.image), cmap=cm.gray)
        return self

    # Plots found components
    def plotComponents(self, Components, img):
        for i in range(len(Components)):
            print(Components[i].componentType)
            y, x = Components[i].centroid
            plt.scatter(x, y, c='r', s=10)
            top, bottom, left, right = Components[i].getRegion(img)
            plt.plot((left, right), (top, top), c='r')
            plt.plot((left, right), (bottom, bottom), c='r')
            plt.plot((left, left), (top, bottom), c='r')
            plt.plot((right, right), (top, bottom), c='r')
        return self

    # Plots found wires
    def plotWires(self, HorizWires, VertWires):
        for wire in HorizWires:
            top, bottom, left, right = wire.line
            plt.plot((left, right), (top, bottom))

        for wire in VertWires:
            top, bottom, left, right = wire.line
            plt.plot((left, right), (top, bottom))
        return self

    # Plots found junctions
    def plotJunctions(self, Junctions, Letters=True):

        for i in range(len(Junctions)):
            y, x = Junctions[i].centroid
            plt.scatter(x, y, c='g', s=50)
            if Letters:
                plt.text(x, y, s=Junctions[i].id, c='blue', size='xx-large')
        return self

    # Retrieve network graph
    def getNetworkGraph(self, Junctions, Components, draw=False):
        # display a network graph of found circuit

        nodes = getNodes(Junctions)
        edges = getEdges(nodes, Components)

        finalNodes = []
        for node in nodes:
            node_entry = node.id, {'subset': node.subset}
            finalNodes.append(node_entry)

        G = nx.MultiDiGraph()
        G.add_nodes_from(finalNodes)
        G.add_edges_from(edges)

        edge_labels = nx.get_edge_attributes(G, 'edge_label')
        formatted_edge_labels = {(elem[0], elem[1]): edge_labels[elem] for elem in edge_labels}

        pos = nx.multipartite_layout(G, align='horizontal', )
        if draw:
            if not len(plt.get_fignums()) == 0:
                figs = plt.get_fignums()
                plt.figure(len(figs) + 1)
            nx.draw_networkx_edges(G, pos, edgelist=G.edges(), connectionstyle='arc3, rad = 0.1')
            nx.draw_networkx_nodes(G, pos, )
            nx.draw_networkx_edge_labels(G, pos, edge_labels=formatted_edge_labels, label_pos=0.3)
            nx.draw_networkx_edges(G, pos, edgelist=G.edges(), connectionstyle='arc3, rad = 0.1')
            nx.draw_networkx_labels(G, pos)
        networkGraph = Graph(G, Components)
        return networkGraph

    # Plots network graph in one subplot, plots image, wires, components and junctions w/ letters in the other
    def plotAll(self, Junctions, Components, HorizWires, VertWires, image):
        plt.close('all')

        # Plot network graph
        fig, axes = plt.subplots(1, 2, figsize=(15, 5), sharex=False, sharey=False)
        ax = axes.ravel()

        nodes = getNodes(Junctions)

        edges = getEdges(nodes, Components)

        G = nx.MultiDiGraph()
        G.add_edges_from(edges)

        edge_labels = nx.get_edge_attributes(G, 'edge_label')
        formatted_edge_labels = {(elem[0], elem[1]): edge_labels[elem] for elem in edge_labels}

        for n in G.nodes:
            for node in nodes:
                if n == node.id:
                    G.nodes[n]['subset'] = node.subset

        pos = nx.multipartite_layout(G, align='horizontal', center=(image.width / 2, image.height / 2))
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), connectionstyle='arc3, rad = 0.1', ax=ax[0])
        nx.draw_networkx_nodes(G, pos, ax=ax[0])
        nx.draw_networkx_edge_labels(G, pos, edge_labels=formatted_edge_labels, label_pos=0.3, ax=ax[0])
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), connectionstyle='arc3, rad = 0.1', ax=ax[0])
        nx.draw_networkx_labels(G, pos, ax=ax[0])
        ax[0].set_title('Network Graph')

        ax[1].set_title('Circuit Schematic')
        ax[1].imshow(image.image, cmap=cm.gray)
        ax[1].set_xlim((0, image.width))
        ax[1].set_ylim((image.height, 0))

        # Plot component bounding boxes
        for i in range(len(Components)):
            print(Components[i].componentType)
            y, x = Components[i].centroid
            ax[1].scatter(x, y, c='r', s=10)
            top, bottom, left, right = Components[i].getRegion(image)
            ax[1].plot((left, right), (top, top), c='r')
            ax[1].plot((left, right), (bottom, bottom), c='r')
            ax[1].plot((left, left), (top, bottom), c='r')
            ax[1].plot((right, right), (top, bottom), c='r')

        # Plot junctions
        for i in range(len(Junctions)):
            y, x = Junctions[i].centroid
            ax[1].scatter(x, y, c='g', s=50)
            ax[1].text(x, y, s=Junctions[i].id, c='red', size='xx-large')

        # Plot wires
        for wire in HorizWires:
            top, bottom, left, right = wire.line
            plt.plot((left, right), (top, bottom))

        for wire in VertWires:
            top, bottom, left, right = wire.line
            plt.plot((left, right), (top, bottom))
        return self, G


# Network X matrix handling class
class Graph:
    def __init__(self, G, components):
        self.componentList = components
        self.graph = G
        self.nodes = G.nodes
        self.edges = G.edges
        self.SP = self.getSpanningTree(draw=False)
        self.CH = self.getCoTree(draw=False)
        self.Bt = self.getIMatrix(self.SP, Reduced=True)
        self.Bc = self.getIMatrix(self.CH, Reduced=True)
        self.referenceVertexSP = self.getIMatrix(self.SP, returnRefVertex=True)
        self.referenceVertexCH = self.getIMatrix(self.CH, returnRefVertex=True)
        self.Df, self.Cf = [], []

    def getIMatrix(self, Graph, Reduced=True, returnRefVertex=False):

        # get sparse matrix
        incidence_matrix_sparse = nx.incidence_matrix(Graph, oriented=True, edgelist=Graph.edges())

        # get dense matrix, reverse convention
        incidence_matrix = incidence_matrix_sparse.todense()
        incidence_matrix = incidence_matrix * -1

        # get reduced matrix:
        incidence_matrix_reduced = np.delete(incidence_matrix, 0, 0)
        incidence_matrix_reduced = np.matrix(incidence_matrix_reduced)

        # get reference vertex (first node since top row is removed)
        reference_vertex = list(Graph.nodes())[0]

        if returnRefVertex:
            return reference_vertex
        elif Reduced:
            return incidence_matrix_reduced
        else:
            return incidence_matrix

    def getSpanningTree(self, draw=False):
        G_edges = self.graph.edges
        nodeSubsetValues = list(self.graph.nodes('subset'))
        nodes = []
        for nSV in nodeSubsetValues:
            node = nSV[0], {'subset': nSV[1]}
            nodes.append(node)

        # get spanning tree in formatted list of edges
        G_Undirected = self.graph
        SP_edges = list(nx.minimum_spanning_edges(G_Undirected.to_undirected()))
        spanning_tree_edge_list = []

        # check all edges against original edge list for correct directionality, fix and incorrect directions then add to list
        for SP_edge in SP_edges:
            for G_edge in G_edges:
                if SP_edge[0] == G_edge[1] and SP_edge[1] == G_edge[0] and SP_edge[2] == G_edge[2]:

                    formatted_edge = SP_edge[1], SP_edge[0], SP_edge[2], SP_edge[3]
                    spanning_tree_edge_list.append(formatted_edge)
                elif SP_edge[0] == G_edge[0] and SP_edge[1] == G_edge[1] and SP_edge[2] == G_edge[2]:

                    formatted_edge = SP_edge[0], SP_edge[1], SP_edge[2], SP_edge[3]
                    spanning_tree_edge_list.append(formatted_edge)

        # create spanning tree graph
        SP = nx.MultiDiGraph()
        # add original node list (### this only works if spanning tree contains all nodes from original graph ###)
        SP.add_nodes_from(nodes)
        # add formatted edge list for spanning tree
        SP.add_edges_from(spanning_tree_edge_list)
        # multi partite layout
        pos = nx.multipartite_layout(SP, align='horizontal')
        if draw:
            if not len(plt.get_fignums()) == 0:
                figs = plt.get_fignums()
                plt.figure(len(figs) + 1)

            # retrieve new edge labels
            sp_edge_labels = nx.get_edge_attributes(SP, 'edge_label')
            # format edge labels
            formatted_edge_labels = {(elem[0], elem[1]): sp_edge_labels[elem] for elem in sp_edge_labels}
            # draw edges and labels
            nx.draw_networkx_edges(SP, pos, edgelist=SP.edges(), connectionstyle='arc3, rad = 0.1')
            nx.draw_networkx_edge_labels(SP, pos, edge_labels=formatted_edge_labels, label_pos=0.3)
            # draw nodes and labels
            nx.draw_networkx_nodes(SP, pos)
            nx.draw_networkx_labels(SP, pos)
        return SP

    def getCoTree(self, draw=False):
        chords = []
        GEdges = nx.get_edge_attributes(self.graph, 'edge_label')
        SPEdges = nx.get_edge_attributes(self.SP, 'edge_label')

        # see if edge is part of spanning tree, if not must be a chord
        for edge in GEdges:
            if edge not in SPEdges:
                chords.append(edge)

        CH = nx.MultiDiGraph()
        CH.add_nodes_from(self.SP.nodes())
        CH.add_edges_from(chords)
        CH_edge_labels = nx.get_edge_attributes(self.graph, 'edge_label')

        # remove labels for non chord edges
        for edge in list(CH_edge_labels):
            e = edge[0], edge[1], edge[2]
            if e not in chords:
                CH_edge_labels.pop(edge)

        formatted_edge_labels = {(elem[0], elem[1]): CH_edge_labels[elem] for elem in CH_edge_labels}

        if draw:
            if not len(plt.get_fignums()) == 0:
                figs = plt.get_fignums()
                plt.figure(len(figs) + 1)

            pos = nx.multipartite_layout(self.graph, align='horizontal')
            nx.draw_networkx_edges(CH, pos, edgelist=CH.edges(), connectionstyle='arc3, rad = 0.1')
            nx.draw_networkx_nodes(CH, pos, )
            nx.draw_networkx_edge_labels(CH, pos, edge_labels=formatted_edge_labels, label_pos=0.3)
            nx.draw_networkx_labels(CH, pos)

        return CH

    def getFundamentalMatrices(self):
        nodeList = removeRedundantNodes(self.graph.edges(), self.graph.nodes)

        # get fundamental cut-set matrix
        Idf = np.identity(len(nodeList) - 1)
        print(Idf.shape)
        print(self.Bt.I.shape)
        print(self.Bc.shape)
        Df = np.hstack((Idf, self.Bt.I @ self.Bc))
        self.Df = Matrix(Df)

        # get fundamental cycle matrix
        Icf = np.identity(len(self.graph.edges) - len(nodeList) + 1)
        Cf = np.hstack((-1 * (self.Bt.I @ self.Bc).T, Icf))
        self.Cf = Matrix(Cf)

        return self.Df, self.Cf

    def linEquations(self):  # put equation stuff from get fund matrix in here
        finalCurrentMatrix = []
        finalVoltageMatrix = []
        currentColumnVector = []
        voltageColumnVector = []

        # get currents column vector
        SP_Edges = list(self.SP.edges)
        CH_Edges = list(self.CH.edges)
        for edge in SP_Edges:
            currentColumnVector.append("i" + str(edge[2]))
            voltageColumnVector.append("v" + str(edge[2]))

        for edge in CH_Edges:
            currentColumnVector.append("i" + str(edge[2]))
            voltageColumnVector.append("v" + str(edge[2]))

        # Transpose column vectors, convert to sympy matrices
        currentColumnVector = np.matrix(currentColumnVector)
        voltageColumnVector = np.matrix(voltageColumnVector)
        currentColumnVector = currentColumnVector.T
        voltageColumnVector = voltageColumnVector.T
        currentColumnVector = Matrix(currentColumnVector)
        voltageColumnVector = Matrix(voltageColumnVector)

        # Multiple Df and current column vector matrices
        LinIndependentCurrentEquations = self.Df * currentColumnVector

        # Multiple Cf and voltage column vector matrices
        LinIndependentVoltageEquations = self.Cf * voltageColumnVector

        # Remove 1.0* coefficients to format nicely
        for equation in LinIndependentCurrentEquations:
            elements = str(equation).split('1.0*')
            elements = ''.join(elements)
            finalCurrentMatrix.append(elements)

        for equation in LinIndependentVoltageEquations:
            elements = str(equation).split('1.0*')
            elements = ''.join(elements)
            finalVoltageMatrix.append(elements)

        finalCurrentMatrix = np.matrix(finalCurrentMatrix)
        finalCurrentMatrix = finalCurrentMatrix.T
        finalCurrentMatrix = Matrix(finalCurrentMatrix)

        finalVoltageMatrix = np.matrix(finalVoltageMatrix)
        finalVoltageMatrix = finalVoltageMatrix.T
        finalVoltageMatrix = Matrix(finalVoltageMatrix)

        return finalCurrentMatrix, finalVoltageMatrix

    def componentMatrix(self, components):
        currentColumnVector = []
        voltageColumnVector = []

        # get current and voltage column vectors
        edgeList = list(self.SP.edges) + list(self.CH.edges)

        for edge in edgeList:
            currentColumnVector.append("i" + str(edge[2]))
            voltageColumnVector.append("v" + str(edge[2]))

        # combine current and voltage column vectors
        voltageColumnVector = np.matrix(voltageColumnVector).T
        currentColumnVector = np.matrix(currentColumnVector).T
        combinedColumnVector = np.vstack((voltageColumnVector, currentColumnVector))

        # Identity matrix
        I = Matrix(np.identity(len(self.graph.edges)))

        # Generate matrix for each component equation
        componentEQMatrix = []
        resultColumnVector = Matrix(np.zeros((2 * len(edgeList), 1)))

        matrixCounter = 0
        for edge in edgeList:

            component_id = edge[2] - 1
            blank_matrix_1d = Matrix(np.zeros((1, len(edgeList))))

            if components[component_id].componentType == 'Resistor (EU)' or components[
                component_id].componentType == 'Resistor (US)':
                blank_matrix_1d[matrixCounter] = '-R' + str(edge[2])

                if matrixCounter == 0:
                    componentEQMatrix = blank_matrix_1d
                else:
                    componentEQMatrix = Matrix.vstack(componentEQMatrix, blank_matrix_1d)
                matrixCounter += 1

            elif components[component_id].componentType == 'Source' or components[component_id].componentType == 'Cell':
                resultColumnVector[matrixCounter] = '-V'
                if matrixCounter == 0:
                    componentEQMatrix = blank_matrix_1d
                else:
                    componentEQMatrix = Matrix.vstack(componentEQMatrix, blank_matrix_1d)
                matrixCounter += 1

            elif components[component_id].componentType == 'Inductor':

                blank_matrix_1d[matrixCounter] = '1/L' + str(edge[2])
                if matrixCounter == 0:
                    componentEQMatrix = blank_matrix_1d
                else:
                    componentEQMatrix = Matrix.vstack(componentEQMatrix, blank_matrix_1d)
                matrixCounter += 1

            elif components[component_id].componentType == 'Capacitor':

                blank_matrix_1d[matrixCounter] = '1/C' + str(edge[2])
                if matrixCounter == 0:
                    componentEQMatrix = blank_matrix_1d
                else:
                    componentEQMatrix = Matrix.vstack(componentEQMatrix, blank_matrix_1d)

                matrixCounter += 1

        # Stack identity matrix

        componentEQMatrix = Matrix.hstack(I, componentEQMatrix)

        # V stack Df matrix under component matrix
        componentEQ_Df_Matrix = Matrix.vstack(componentEQMatrix,
                                              Matrix.hstack(self.Cf, Matrix(np.zeros(self.Cf.shape))))

        # V stack Cf matrix under component & Df matrix
        componentEQ_Df_Cf_Matrix = Matrix.vstack(componentEQ_Df_Matrix,
                                                 Matrix.hstack(Matrix(np.zeros(self.Df.shape)), self.Df))

        return componentEQ_Df_Cf_Matrix, combinedColumnVector, resultColumnVector

    def getComponentEquations(self, matrices=False):
        H, x, y = self.componentMatrix(self.componentList)
        componentEquations = Matrix.hstack(
            (nsimplify(Matrix(np.identity(2 * len(self.componentList))) * (H.inv() * y)).evalf(3)),
            Matrix(x)).evalf(3)
        if matrices:
            return H, x, y, componentEquations
        else:
            return componentEquations


# Found Component Class
class Component:

    def __init__(self, component):
        self.path = ''
        self.id = 0
        self.centroid = component
        self.centroidY, self.centroidX = component
        self.Height = config.componentWidth
        self.Width = config.componentWidth
        self.isVert = False
        self.associatedHWires = []
        self.associatedVWires = []
        self.componentType = ''
        self.unichar = ''
        self.terminalNo = 2

    def getRegion(self, Image):

        self.top = math.ceil(self.centroidY - (self.Height / 2))
        self.bottom = math.ceil(self.centroidY + (self.Height / 2))
        self.left = math.ceil(self.centroidX - (self.Width / 2))
        self.right = math.ceil(self.centroidX + (self.Width / 2))
        if self.top < 0:  self.top = 0
        if self.bottom > Image.height:  self.bottom = Image.height
        if self.left < 0:  self.left = 0
        if self.right > Image.width:  self.right = Image.width

        componentRegion = self.top, self.bottom, self.left, self.right
        return componentRegion


# Hough Lines Class - Horizontal
class HorizontalLines:
    def __init__(self, x1, y1, x2, y2):
        self.line = x1, y1, x2, y2
        self.length = math.hypot(abs(x2 - x1), abs(y1 - y2))
        self.centre = float(self.length / 2)
        self.start = y1, x1
        self.end = y2, x2
        self.inBox = False
        self.inPair = False


# Hough Lines Class - Vertical
class VerticalLines:
    def __init__(self, x1, y1, x2, y2):
        self.line = x1, y1, x2, y2
        self.length = math.hypot(abs(x2 - x1), abs(y1 - y2))
        self.centre = float(self.length / 2)
        self.start = y1, x1
        self.end = y2, x2
        self.inBox = False
        self.inPair = False


# Horizontal Wires Class
class WireHoriz:
    def __init__(self, y1, y2, x1, x2, binaryImage):
        self.wire = binaryImage[y1:y2, x1:x2]
        self.length = binaryImage[y1:y2, x1:x2].shape[1]
        self.centre = int(x1 + ((x2 - x1) / 2))
        self.line = y1, y2, x1, x2
        self.start = y1, x1
        self.end = y2, x2

    def getBorder(self):
        rows = np.any(self.wire, axis=0)
        columns = np.any(self.wire, axis=1)
        left, right = np.where(rows)[0][[0, -1]]
        top, bottom = np.where(columns)[0][[0, -1]]
        wireBorder = [top, bottom, left, right]
        return wireBorder


# Vertical Wires Class
class WireVert:
    def __init__(self, y1, y2, x1, x2, binaryImage):
        self.wire = binaryImage[y1:y2, x1:x2]
        self.length = binaryImage[y1:y2, x1:x2].shape[1]
        self.centre = int(y1 + ((y2 - y1) / 2))
        self.line = y1, y2, x1, x2
        self.start = y1, x1
        self.end = y2, x2

    def getBorder(self):
        rows = np.any(self.wire, axis=0)
        columns = np.any(self.wire, axis=1)
        left, right = np.where(rows)[0][[0, -1]]
        top, bottom = np.where(columns)[0][[0, -1]]
        wireBorder = [top, bottom, left, right]
        return wireBorder


# Wire Junctions class
class WireJunctions:
    def __init__(self, centroid):
        self.id = ''
        self.id_node = ''
        self.centroid = centroid[0], centroid[1]
        self.terminals = 0
        self.directions = 'NIL'  # N, S, E, W ->> north is up, south is down, west/east are left/right
        self.type = 'NIL'  # Corner, tri junction, quad junction
        self.associatedHWires = []
        self.associatedVWires = []
        self.isNode = True
        self.connectedNodesH = []
        self.connectedNodesV = []
