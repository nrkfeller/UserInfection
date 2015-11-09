#Khan Academy
###Interview project
Technologies used: 
* neo4j
* Ipython notebook
* p2neo (python neo4j api's)
* networkx

This project creates users that are to be 'infected' with a new feature. The features can infect either a set amount of users (limited_infection) or the entire population (total_infection).
Each user is a node in the neo4j database. When a user is coaching another user, they have a single directed relationship.
When limited infection is initiated, all users grouped by a coaching relationship must be infected, regardless of direction.

What this project does:
1. Create a user class that has attributes and behaviors when being infected.
2. Creates a certain amount of users and pseudo-randomly creates relationships. This is done in the hopes or replicating (in a smaller scale) what the actualy user population relationships might look like.
3. Test limited infection on a set number of users. If the set number of users is possible given the coaching relationship constraints, infect thoser users. Show visualization
4. Test total infection, infect the remaining users. Show visualization

##What it looks like in Neo4j DB
####Initial population:
![Image of Yaktocat](https://github.com/nrkfeller/UserInfection/blob/master/InitialPopulation.png)

####Partial infection:
![Image of Yaktocat](https://github.com/nrkfeller/UserInfection/blob/master/PartialInfection.png)

####Total infection:
![Image of Yaktocat](https://github.com/nrkfeller/UserInfection/blob/master/FullInfection.png)