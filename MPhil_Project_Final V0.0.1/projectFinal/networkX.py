# -*- coding: utf-8 -*-
"""
NetworkX
========

A toolkit of functions for converting an analysed circuit into a network graph

author: C. R. Kelly
email: CK598@cam.ac.uk

"""
import networkx as nx

from .config import Config

config = Config()


# NetworkX Nodes class
class Nodes:
    def __init__(self, id):
        self.id = id
        self.subset = 0
        self.associatedHWires = []
        self.associatedVWires = []


def getNodeSubsets(nodes):
    """ Assign associated multi partite subsets to node.subset_id for every node

    :param nodes: list: List of nodes returned by getNodes(junctions)

    """
    # create new list of nodes, and their y values to work on
    nodeTempList = []
    nodeSubsetList = []
    for node in nodes:
        yval = 0
        if len(node.associatedHWires) == 1:
            yval = node.associatedHWires[0].line[0]
        elif len(node.associatedHWires) > 1:
            total = 0
            for wire in node.associatedHWires:
                total += wire.line[0]
            yval = total / len(node.associatedHWires)

        nodeTempList.append((node.id, yval, 0))

    # bubble sort to have node list in increasing order of y values
    for i in range(len(nodeTempList) ** 2):
        for j in range(len(nodeTempList) - 1):
            if nodeTempList[j][1] > nodeTempList[j + 1][1]:
                a0 = nodeTempList[j][0], nodeTempList[j][1]
                a1 = nodeTempList[j + 1][0], nodeTempList[j + 1][1]
                nodeTempList[j], nodeTempList[j + 1] = a1, a0

    # write function to set node.subset to value

    subset_counter = 0
    node_yval_counter = 0
    for i in range(0, len(nodeTempList)):
        if node_yval_counter >= len(nodeTempList):
            break
        yval = nodeTempList[node_yval_counter][1]
        for n2 in nodeTempList:
            if n2[1] == yval:
                node_yval_counter += 1
                n2 = n2[0], n2[1], subset_counter
                nodeSubsetList.append(n2)
        subset_counter -= 1
    for node in nodes:
        for n in nodeSubsetList:

            if n[0] == node.id:
                node.subset = n[2]


def getNodes(junctions):
    """ Find all corresponding nodes for every detected wire junction

    :param junctions: list: List of junctions returned by junctionDetection(HorizWires, VertWires)
    :return nodes: list: List of nodes
    """
    nodes = []

    # Searching for junctions that are directly connected by a wire (these junctions combine into the same node)
    for junction1 in junctions:
        for junction2 in junctions:
            if not junction1.id == junction2.id:
                if junction1.associatedHWires[0].line == junction2.associatedHWires[0].line:
                    junction1.isNode = False
                    junction2.isNode = False
                    junction1.connectedNodesH.append(junction2.id)
                    junction2.connectedNodesH.append(junction1.id)
                elif junction1.associatedVWires[0].line == junction2.associatedVWires[0].line:
                    junction1.isNode = False
                    junction2.isNode = False
                    junction1.connectedNodesV.append(junction2.id)
                    junction2.connectedNodesV.append(junction1.id)

    for junction in junctions:
        if not junction.isNode:
            # bubble sort horizontal node list to highest node first
            if len(junction.connectedNodesH) > 1:

                for i in range(len(junction.connectedNodesH) ** 2):
                    for j in range(len(junction.connectedNodesH) - 1):
                        if ord(junction.connectedNodesH[j]) > ord(junction.connectedNodesH[j + 1]):
                            junction.connectedNodesH[j], junction.connectedNodesH[j + 1] = junction.connectedNodesH[
                                                                                               j + 1], \
                                                                                           junction.connectedNodesH[j]

            # bubble sort vertical node list to highest node first
            if len(junction.connectedNodesV) > 1:

                for i in range(len(junction.connectedNodesV) ** 2):
                    for j in range(len(junction.connectedNodesV) - 1):
                        if ord(junction.connectedNodesV[j]) > ord(junction.connectedNodesV[j + 1]):
                            junction.connectedNodesV[j], junction.connectedNodesV[j + 1] = junction.connectedNodesV[
                                                                                               j + 1], \
                                                                                           junction.connectedNodesV[j]

            # setting junction.id_node as the highest associated node there is
            if len(junction.connectedNodesH) > 0 and len(junction.connectedNodesV) > 0:

                if ord(junction.connectedNodesV[0]) < ord(junction.connectedNodesH[0]) and ord(
                        junction.connectedNodesV[0]) < ord(junction.id):
                    junction.id_node = junction.connectedNodesV[0]
                elif ord(junction.connectedNodesH[0]) < ord(junction.connectedNodesV[0]) and ord(
                        junction.connectedNodesH[0]) < ord(junction.id):
                    junction.id_node = junction.connectedNodesH[0]
                else:
                    junction.id_node = junction.id

            elif len(junction.connectedNodesH) > 0:
                if ord(junction.connectedNodesH[0]) < ord(junction.id):
                    junction.id_node = junction.connectedNodesH[0]
                else:
                    junction.id_node = junction.id
            elif len(junction.connectedNodesV) > 0:
                if ord(junction.connectedNodesV[0]) < ord(junction.id):
                    junction.id_node = junction.connectedNodesV[0]
                else:
                    junction.id_node = junction.id

    for junction in junctions:
        if junction.isNode and junction.id_node == '':
            junction.id_node = junction.id
        if junction.id_node == junction.id:
            junction.isNode = True

    # Extracting nodes into a list

    for junction in junctions:

        # Adding Nodes into list
        if junction.isNode:
            node = Nodes(junction.id_node)
            node.associatedHWires = junction.associatedHWires
            node.associatedVWires = junction.associatedVWires
            nodes.append(node)

    # Combining directly connected junctions into the same node
    for junction in junctions:

        if not junction.isNode:

            for node in nodes:
                if junction.id_node == node.id and not junction.id_node == '':
                    for wire in junction.associatedHWires:
                        if wire not in node.associatedHWires:
                            node.associatedHWires.append(wire)
                    for wire in junction.associatedVWires:
                        if wire not in node.associatedVWires:
                            node.associatedVWires.append(wire)

    # Reorder node list to remove gaps in the lettering
    label = 'A'
    for node in nodes:
        node.id = label
        label = chr(ord(label) + 1)

    # assign node.subset to node subset
    getNodeSubsets(nodes)

    # reverse node list so graph plots left to right, top to bottom
    nodes = nodes[::-1]

    return nodes


def getEdges(nodes, components):
    """ Find all pairs of nodes that form graph edges for every node.

    :param nodes: list: List of nodes returned by getNodes(junctions).
    :param components: list: List of components returned by objectDetection(HorizWires, VertWires, image, maximumDistance=config.maximumDistance, minimumDistance=config.minimumDistance)
    :return labelledEdges: list: List of labelled edges
    """

    labelledEdges = []
    edges = []
    for component in components:
        if component.terminalNo == 2:
            node1Found = False
            node2Found = False
            if not component.isVert:
                for node in nodes:
                    for wire in node.associatedHWires:
                        if component.associatedHWires[0] == wire:
                            node1 = node.id
                            node1Found = True
                        elif component.associatedHWires[1] == wire:
                            node2 = node.id
                            node2Found = True
                    if node1Found and node2Found:
                        pair = (node1, node2)
                        edges.append(pair)
                        break
            elif component.isVert:
                for node in nodes:
                    for wire in node.associatedVWires:
                        if component.associatedVWires[0] == wire:
                            node1 = node.id
                            node1Found = True
                        elif component.associatedVWires[1] == wire:
                            node2 = node.id
                            node2Found = True
                    if node1Found and node2Found:
                        pair = (node1, node2)
                        edges.append(pair)
                        break

    # if two edges connect the same two nodes, make sure they alternate
    edges = list(edges)
    for edgepos in range(len(edges)):
        if edges.count(edges[edgepos]) > 1:
            for edgepos2 in range(edgepos + 1, len(edges)):
                if edges.count(edges[edgepos2]) > 1:
                    value0, value1 = edges[edgepos2][0], edges[edgepos2][1]
                    edges[edgepos2] = (value1, value0)

    # set edge labels
    edge_label = 0
    for edge in edges:
        node1 = edge[0]
        node2 = edge[1]
        edge = (node1, node2, edge_label, {'edge_label': str(edge_label)})
        labelledEdges.append(edge)
        edge_label += 1

    return labelledEdges


def displayNetworkGraph(junctions, components, multipartiteLayout=True):
    """ Draws network graph of circuit schematic

        :param multipartiteLayout: boolean: Decide whether to use multipartite layout for graph plotting
        :param junctions: list: List of junctions returned by junctionDetectinon(HorizWires, VertWires)
        :param components: list: List of components returned by objectDetection(HorizWires, VertWires, image, maximumDistance=config.maximumDistance, minimumDistance=config.minimumDistance)
        :return labels: list: List of edge labels
    """
    # display a network graph of found circuit

    nodes = getNodes(junctions)

    edges = getEdges(nodes, components)

    G = nx.MultiDiGraph()
    G.add_edges_from(edges)

    edge_labels = nx.get_edge_attributes(G, 'edge_label')
    formatted_edge_labels = {(elem[0], elem[1]): edge_labels[elem] for elem in edge_labels}

    if multipartiteLayout:
        for n in G.nodes:
            for node in nodes:
                if n == node.id:
                    G.nodes[n]['subset'] = node.subset

    pos = nx.multipartite_layout(G, align='horizontal')
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), connectionstyle='arc3, rad = 0.1')
    nx.draw_networkx_nodes(G, pos, )
    nx.draw_networkx_edge_labels(G, pos, edge_labels=formatted_edge_labels, label_pos=0.3)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), connectionstyle='arc3, rad = 0.1')
    nx.draw_networkx_labels(G, pos)


def removeRedundantNodes(edges, nodes):
    """ Removes nodes that don't form edges

    :param edges: list: List of edges.
    :param nodes: list: List of nodes.
    :return list: Returns list of used nodes
    """
    Edges = []
    presentNodes = []
    edges = list(edges)
    nodes = list(nodes)
    for edge in edges:
        for e in range(0, len(edge)):
            Edges.append(edge[e])

    for node in nodes:
        if node in Edges:
            presentNodes.append(node)

    return presentNodes
