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



# INFECT ALL USERS THAT ARE NOT YET INFECTED
def total_infection():
    """
    Infect all users that are not yet infected
    This can be done much faster with a simple Cypher instruction, but would not have the effect
    of re-creating the nodes as a UserB node in the graph database.
    """
    for user in AllUsers:
        if (user.khanAcademyVersion == 'A'):
            user.infect()
            
    visualizeNXGraph()