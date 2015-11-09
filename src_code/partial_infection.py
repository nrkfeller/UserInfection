from userclass import User
from py2neo import Node, Relationship, Path, Rev
from py2neo import authenticate, Graph
from itertools import *
import requests
import numpy as np
import unicodedata
import numpy as np
import time
import datetime
import random
import names
import matplotlib.pyplot as plt
import networkx as nx
%matplotlib inline


#INFECT ARGUMENT PASSED NUMBER OF USERS
def partial_infection(usersToInfect):
    
    # get all subgraph in a dictionary
    subgraphs = grabSubgraphs()
    # place them in a list for computation
    list(subgraphs.values())

    # get all the possible combinations that can result in the value passing in the argument 'usersToInfect'
    c = chain(*[combinations(list(subgraphs.values()), i) for i in range(len(list(subgraphs.values()))+1)])
    combinationToInfect = [n for n in c if sum(n) == usersToInfect]

    # crawl through and infect the selected subgraphs
    if (len(combinationToInfect) > 0):
        for name, val in subgraphs.items():
            if val in combinationToInfect[0]:
                for user in AllUsers:
                    if user.name == name:
                        crawl(user)
    # tell user if it is not possible to infect exact amount of users
    else:
        print "Not possible to infect exaclty", usersToInfect, "users. Please chose any combination of", list(subgraphs.values())
    
    visualizeNXGraph()
    
    
    
def grabSubgraphs():
    """
    Get all the subgraph size and the name of any node in that subgraph. place into dictionary
    """
    # grab all nodes directly from the database. Only nodes that are in previous version
    nodes = %cypher MATCH n WHERE n.khanAcademyVersion = "B" RETURN n

    # put nodes into a dafaframe and initialize containers for results
    nodes = nodes.dataframe
    allnodes=[]
    subgraphChunks = {}
    
    # put the rows from the dataframe into a list
    for index, row in nodes.iterrows():
        allnodes.append(row[0])
            
    # grab a name associated with a subgraph and and the quantity of nodes in that subgraph
    while(len(allnodes) > 0):
        name = unicodedata.normalize('NFKD', allnodes[0]['name']).encode('ascii','ignore')
        subgraph = %cypher MATCH p=(n { name: {name}})-[r*0..]-(m) WITH NODES(p) AS nodes UNWIND nodes AS node RETURN DISTINCT node
        subgraph = subgraph.dataframe
        subarray = []
        for index, row in subgraph.iterrows():
            subarray.append(row[0])
        allnodes = filter(lambda x:x not in subarray, allnodes)
        subgraphChunks[name] = len(subarray)
    return subgraphChunks


def crawl(user):
    """
    Recursively infect everyone with a coach or student relationship
    """
    iuser = user
    iuser.infect()
    for u in user.coaches:
        if u.khanAcademyVersion == 'A':
            crawl(u)
    for u in user.students:
        if u.khanAcademyVersion == 'A':
            crawl(u)