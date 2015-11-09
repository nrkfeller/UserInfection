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

# GENERATE 200 USERS AND GIVE THEM PSEUDO RANDOM RELATIONSHIPS
def generateUsers(numberOfUsers):
    """
    Create n fake users (n = argument numer) and gives them some pseudo random relationships.
    then remove the users that have no relationships. This is so that we can test the failure
    of the limited infection method.
    """
    AllUsers = []
    Users = []

    # make 200 users and place them in an array
    for i in range(0,numberOfUsers):
        newUser = User()
        Users.append(newUser)
        
    AllUsers.extend(Users)
    # create relationships between relationship-less nodes remaining in the database
    def createRelationships(Users):
        i = 1
        for u in Users:
            i = i+1
            if (i%15 == 0):
                potentialRels = map(lambda x: random.randint(-8,8), np.zeros(random.randint(0,10)))
                set(potentialRels)
                for num in potentialRels:
                    u.isCoaching(Users[(i+num)%len(Users)])
                    #graph.create(Relationship(u.databaseNode, "IS_COACHING", Users[(i+num)%len(Users)].databaseNode))

    # until we have only a few remaining nodes without relationships
    while (len(Users) > 20):
        remaining = []

        createRelationships(Users)

        for u in Users:
            for j in u.databaseNode.match_incoming(rel_type=None, start_node=None, limit=None):
                if (len(j) != 0):
                    remaining.append(u)
        Users = list(set(Users) - set(remaining))
        
    # this cypher instruction deletes all nodes that have no relationships.
    # we could keep them, but it's better to test features on users that have relationships
    cypher.execute("MATCH (n) WHERE size((n)--())=0 DELETE (n)")

    visualizeNXGraph()
    
    return AllUsers

   
generateUsers(200)