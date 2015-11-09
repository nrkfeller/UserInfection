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

# Interact with neo4j database directly
%load_ext cypher
authenticate("localhost:7474", "neo4j", "neo4j")
graph = Graph("http://localhost:7474/db/data/")
cypher = graph.cypher

#USER CLASS

class User:
    
    """
    Creates a User
    User has attributes Name, Version and Last Login
    When user is creates, a database node is created in Neo4j
    When user is infected, the node is remove and replaced by new node (version update)
    """
    
    # Initializer
    def __init__(self):
        
        # Give user a full name. Generated randomly
        self.name =  unicodedata.normalize('NFKD', names.get_full_name()).encode('ascii','ignore')
        
        # Current base version of the website
        self.khanAcademyVersion = 'A'
        
        # keep all students in a set
        self.students = set()
        
        # keep all coaches in a set
        self.coaches = set()
        
        # Number of loggins, int days ago
        self.lastLogin = random.randint(0,50)
        
        ######################DATABASE#######################
        
        # Save this user as a node in the graph database
        self.databaseNode = Node("UserA", name = self.name, khanAcademyVersion = self.khanAcademyVersion, LastLogin = self.lastLogin)
        graph.create(self.databaseNode)
        
        
        
    def isCoaching(self, student):
        
        if (student != self and (student not in self.students or self not in student.coaches)):
            self.students |= {student}
            student.coaches |= {self}
        
        ######################DATABASE#######################
            graph.create(Relationship(self.databaseNode, "IS_COACHING", student.databaseNode))
        
    
    def isStudent(self, coach):
        
        if (coach != self and (self not in coach.students or coach not in self.coaches)):
            coach.students |= {self}
            self.coaches |= {coach}
        
        ######################DATABASE#######################
            graph.create(Relationship(coach.databaseNode, "IS_COACHING", self.databaseNode))
    
    #Class method for user infection    
    def infect(self):
        
        # Deploys new version of Khan Academy to this user
        self.khanAcademyVersion = 'B'
        
        ######################DATABASE#######################
        
        # save all relationships, ingoing and outgoing of this node
        incomingRel = self.databaseNode.match_incoming(rel_type="IS_COACHING")
        outgoingRel = self.databaseNode.match_outgoing(rel_type="IS_COACHING")
        
        # create a node that is of typer UserN
        self.databaseNode = Node("UserB", name = self.name, khanAcademyVersion = self.khanAcademyVersion, LastLogin = self.lastLogin)
        graph.create(self.databaseNode)     
        
        # Build the same relationships as the UserA node
        for r in incomingRel:
            startNode = r.start_node
            graph.create(Relationship(startNode, "IS_COACHING", self.databaseNode))
        for r in outgoingRel:
            endNode = r.end_node
            graph.create(Relationship(self.databaseNode, "IS_COACHING", endNode))
        
        
        # Delete the old node
        cypher.execute("MATCH (u :UserA {khanAcademyVersion: {khanAcademyVersion}, name: {name}})-[r]-() DELETE r", khanAcademyVersion = 'A', name = self.name)
        cypher.execute("MATCH n WHERE (n.khanAcademyVersion = {khanAcademyVersion} AND n.name = {name}) DELETE n", khanAcademyVersion = 'A', name = self.name)



# INLINE VISUALIZATION OF CURRENT STATE OF DATABASE WITH NX
def visualizeNXGraph():
    
    results = %cypher MATCH (u)-[r:IS_COACHING]-(n) RETURN u.name, r, n.name

    # get information from the database on visualize it with NetworkX
    
    g = results.get_graph()
    node_map = {'UserA':'green', 'UserB':'red'}
    plt.figure(figsize=(20,10))
    nx.draw(g,pos=nx.shell_layout(g), node_color=[node_map[g.node[node]['labels'][0]] for node in g])
  