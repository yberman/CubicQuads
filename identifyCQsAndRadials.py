#!/usr/local/bin/python


#This program reads in all Known Cubic graphs and tries to match the with extractions from
#a list of known CQs.  It also takes the radials of the CQs.

#It uses networkx:
# https://networkx.github.io/documentation/stable/tutorial.html#creating-a-graph

import networkx as nx
from networkx.algorithms import planarity;

#
# Read in the known cubics.
#

file = open("KnownCubics.txt","r");

allRead = False;

cubic=0;
CubicGraphs = []
title = []
matched = [];

while (not allRead):
    CubicGraphs.append(nx.MultiGraph());
    matched.append(False);
    
    i=-1;
    allRead = True;

    for line in file:
        if (not line.strip()):
            allRead=False;
            break;

        if (i==-1):   # read in the title of the graph
            print "Reading ",line;
            title.append(line);
            i = i+1;
            continue;

        [m,n] = line.split(" ");
        CubicGraphs[cubic].add_edge(int(m),int(n));

    cubic = cubic +1;


#######
#######


file = open("CQsWithoutRadials.txt","r");

allRead = False;

H = nx.MultiGraph();
G = nx.Graph();
I = nx.Graph();

graph = 0;
while (not allRead):
    G.clear();
    i=0;

    allRead=True;
    for line in file:
        if (not line.strip()):
            allRead=False;
            break;


        line2 = line.replace(";","");
        vertex = int(line2.split(":")[0]);
        edges= line2.split(":")[1].split(" ");

        for j in range(1,len(edges)):
            q = int(edges[j]);
            if (vertex < q):
                G.add_edge(vertex,q);
        i=i+1;


    print "Graph = ",graph        
    print G.number_of_nodes();
    print G.number_of_edges();
        
    (isPlanar,PG) = planarity.check_planarity(G);
#    print isPlanar;
#    print PG.check_structure();
    CCW = PG.get_data();

#
# This code takes the radial of G and stores it in the graph I.
#    
    I.clear();
    n = G.number_of_nodes();   # number of edges in original graph.  we will be adding additional points to take the radial.
    marked_edges = set();
    
    for v in CCW:
        for w in CCW[v]:
            if not (v,w) in marked_edges:
                face = PG.traverse_face(v,w,marked_edges);
                print face;
                for q in face:
                    I.add_edge(n,q);
                n=n+1;
                


#
# This code takes the cubic extract of G and stores it in the multigraph H.
#
    H.clear();

    for v in CCW:
#        print v," ",CCW[v];
        if (len(CCW[v]) == 3):
            for q in CCW[v]:
                found = False;
                m = q;
                n = v;
                while (not found):
                    if (len(CCW[m]) == 3):
                        found = True;
                        if (v <= m):
                            print v," ",m;
                            H.add_edge(v,m);
                    else:   # degree 4 vertex.
                        for i in range(0,4):
                            if (n == CCW[m][i]):
                                n = m;
                                m = CCW[m][(i+2)%4]
                                break;

#
# This code compares the cubic extract in H with the list of all known cubics and outputs the title.
#
                            
    found = False;                            
    for cubic in range(0, len(CubicGraphs)):
        if (nx.is_isomorphic(CubicGraphs[cubic],H)):
            found = True;
            matched[cubic] = True;
            print cubic, len(title),len(CubicGraphs);
            print title[cubic];

    if (not found):
        print "Not found";

                
    print "New number of vertices: ", I.number_of_nodes();
    print "New number of edges: ",I.number_of_edges();

    (isPlanar,PG) = planarity.check_planarity(I);
#    print "New graph is planar: ",isPlanar;
    
    
#
# This code prints out the face list of I, the radial.
#  
    H.clear();
    # Extract
    CCW = PG.get_data();

    for v in CCW:
        for w in CCW[v]:
            if not (v,w) in marked_edges:
                face = PG.traverse_face(v,w,marked_edges);
                print face;


    for v in CCW:
#        print v," ",CCW[v];
        if (len(CCW[v]) == 3):
            for q in CCW[v]:
                found = False;
                m = q;
                n = v;
                while (not found):
                    if (len(CCW[m]) == 3):
                        found = True;
                        if (v <= m):
                            H.add_edge(v,m);
                            print v," ",m;
                    else:   # degree 4 vertex.
                        for i in range(0,4):
                            if (n == CCW[m][i]):
                                n = m;
                                m = CCW[m][(i+2)%4]
                                break;

    print "";

    found = False;
    for cubic in range(0, len(CubicGraphs)):
        if (nx.is_isomorphic(CubicGraphs[cubic],H)):
            found = True;
            matched[cubic] = True;
            print cubic, len(title);
            print title[cubic];

    if (not found):
        print "Not found";

    graph=graph+1;


print "Cubics for which we could not find a CQ are:"
for cubic in range(0,len(CubicGraphs)-1):
    if (not matched[cubic]):
        print title[cubic];
