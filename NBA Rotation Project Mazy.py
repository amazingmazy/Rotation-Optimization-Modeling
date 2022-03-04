#!/usr/bin/env python
# coding: utf-8

# > Title: *Building an optimal rotation for the Denver Nuggets* <br>
# > Author: *Anthony Mazy* <br>
# > Date: *Winter Quarter 2020* <br>

# # Table of Contents<a id="Top"></a>
# 
# 1. [Problem Statement](#1)<br>
# 2. [Data](#2) <br>
#     2.1 [Data Source](#2.1)<br>
# 3. [Model Definition](#3)<br>
# 4. [Model Solution](#4)<br>
# 5. [Sensitivity Analysis](#5)<br>
#     5.1 [Change MPJ's Adj RPM](#5.1)<br>
#     5.2 [Remove 15 Minute Per Game Bonus](#5.2)<br>
#     5.3 [Raise limit for how many Minutes a Player Can Play to 40](#5.3)<br>
# 6. [Conclusions](#6)<br>
#     6.1 [Tactical Information](#6.1)<br>
#     6.2 [Strategic Information](#6.2)<br>
# 7. [Model Limitations, Future Improvements and Challenges](#7) <br>

# # 1. Problem Statement<a id=1></a>

# Each basketball team must build a roration, an assignment of how many minutes each player on the team will play per night. The sum total of the minutes each player will plays is bound to 240 minutes as the team must play 5 players for the duration of the 48 minute game
# 
# The central problem is to build a rotaion for the Denver Nuggets with the primary goal of creating the best performing team. The basis for this model will be Real Plus Minus (RPM), an advanced stat meant to measure the overall effect a player has on their team, which I will adjust for minutes played (Adj. RPM). The sum product of each players Adj. RPM and Their Minutes Played will be the foremost .
# 

# ##### [Back to Top](#Top)

# # 2. Data<a id=2></a>

# ## 2.1 Data Source<a id=2.1></a>

# the data comes from ESPN.com here is the link to the Data:
# http://www.espn.com/nba/statistics/rpm
# 

# In[58]:


import pandas as pd
import pyomo.environ as pe
raw_data = pd.read_excel('FinalData.xlsx', sheet_name='Sheet1')
raw_data


# In[59]:


data = pd.DataFrame(raw_data.iloc[6:21, 5])
data.columns = ['Adj. RPM']
data.index = raw_data.iloc[6:21, 2]

# note players arw pre-sorted by minutes adjusted Real Plus Minus
data


# ##### [Back to Top](#Top)

# # 3. Model Definition<a id=3><a>

# In the rotation each player will be assigned a certain quantity of minutes. The objective will essentially be the sum product of every players minutes assigned and their adjusted Real Plus Minus. subject to certain constraints and adjustments. The first of these constraints is simply no player can play over 36 minutes as they will become to tired. Additionally, the coaching staff has stated the value in a deep rotation (is a rotation in which many players play significant minutes) for the sake of team morale. As such an additional a point point will be added to the objective function for every player who plays 5 minutes or more per game and an additional point for every player who plays 15 minutes or more. Additionally, management has identified Michael Porter Jr. as a player with immense potential and as such I will add an 3 points if he plays 15 or more more. Other constraints are that no player may may play more minutes than another who has a higher Real Pus Minus adjusted for minutes played this is because an objectively worse player playing more minutes will decrease team morale. Finally, the sum of all the players' assigned minutes will be bound to to 240 becaue there are 48 minutes in a game and 
# 
# 

# In[60]:


# Craete Pyomo Model and Build It Objective and Comstraints
model = pe.ConcreteModel()
decision_index = range(15)

model.mins = pe.Var(decision_index, domain=pe.Integers, bounds=(0,36))
model.bin5 = pe.Var(decision_index, domain=pe.Binary)
model.bin15 = pe.Var(decision_index, domain=pe.Binary)
model.binMPJ = pe.Var(domain=pe.Binary)


#CONSTRAINTS

# Total Mins Played == 240
model.tot_mins = pe.Constraint(expr=sum(model.mins[i] for i in decision_index) == 240)
    
# constraints that force a player to play over 5 mins per game if they get the over 5 min bonus
model.cons_five_0 = pe.Constraint(expr=(model.bin5[0]*5) <= (model.mins[0]))
model.cons_five_1 = pe.Constraint(expr=(model.bin5[1]*5) <= (model.mins[1]))
model.cons_five_2 = pe.Constraint(expr=(model.bin5[2]*5) <= (model.mins[2]))
model.cons_five_3 = pe.Constraint(expr=(model.bin5[3]*5) <= (model.mins[3]))
model.cons_five_4 = pe.Constraint(expr=(model.bin5[4]*5) <= (model.mins[4]))
model.cons_five_5 = pe.Constraint(expr=(model.bin5[5]*5) <= (model.mins[5]))
model.cons_five_6 = pe.Constraint(expr=(model.bin5[6]*5) <= (model.mins[6]))
model.cons_five_7 = pe.Constraint(expr=(model.bin5[7]*5) <= (model.mins[7]))
model.cons_five_8 = pe.Constraint(expr=(model.bin5[8]*5) <= (model.mins[8]))
model.cons_five_9 = pe.Constraint(expr=(model.bin5[9]*5) <= (model.mins[9]))
model.cons_five_10 = pe.Constraint(expr=(model.bin5[10]*5) <= (model.mins[10]))
model.cons_five_11 = pe.Constraint(expr=(model.bin5[11]*5) <= (model.mins[11]))
model.cons_five_12 = pe.Constraint(expr=(model.bin5[12]*5) <= (model.mins[12]))
model.cons_five_13 = pe.Constraint(expr=(model.bin5[13]*5) <= (model.mins[13]))
model.cons_five_14 = pe.Constraint(expr=(model.bin5[14]*5) <= (model.mins[14]))

# constraints that force a player to play over 15 mins per game if they get the over 15 min bonus
model.cons_fifteen_0 = pe.Constraint(expr=(model.bin15[0]*15) <= (model.mins[0]))
model.cons_fifteen_1 = pe.Constraint(expr=(model.bin15[1]*15) <= (model.mins[1]))
model.cons_fifteen_2 = pe.Constraint(expr=(model.bin15[2]*15) <= (model.mins[2]))
model.cons_fifteen_3 = pe.Constraint(expr=(model.bin15[3]*15) <= (model.mins[3]))
model.cons_fifteen_4 = pe.Constraint(expr=(model.bin15[4]*15) <= (model.mins[4]))
model.cons_fifteen_5 = pe.Constraint(expr=(model.bin15[5]*15) <= (model.mins[5]))
model.cons_fifteen_6 = pe.Constraint(expr=(model.bin15[6]*15) <= (model.mins[6]))
model.cons_fifteen_7 = pe.Constraint(expr=(model.bin15[7]*15) <= (model.mins[7]))
model.cons_fifteen_8 = pe.Constraint(expr=(model.bin15[8]*15) <= (model.mins[8]))
model.cons_fifteen_9 = pe.Constraint(expr=(model.bin5[9]*15) <= (model.mins[9]))
model.cons_fifteen_10 = pe.Constraint(expr=(model.bin15[10]*15) <= (model.mins[10]))
model.cons_fifteen_11 = pe.Constraint(expr=(model.bin15[11]*15) <= (model.mins[11]))
model.cons_fifteen_12 = pe.Constraint(expr=(model.bin15[12]*15) <= (model.mins[12]))
model.cons_fifteen_13 = pe.Constraint(expr=(model.bin15[13]*15) <= (model.mins[13]))
model.cons_fifteen_14 = pe.Constraint(expr=(model.bin15[14]*15) <= (model.mins[14]))

# constraints that force players with higher Adj Real Plus Minus to play more
model.cons_sup0 = pe.Constraint(expr=(model.mins[0]) >= (model.mins[1]))
model.cons_sup1 = pe.Constraint(expr=(model.mins[1]) >= (model.mins[2]))
model.cons_sup2 = pe.Constraint(expr=(model.mins[2]) >= (model.mins[3]))
model.cons_sup3 = pe.Constraint(expr=(model.mins[3]) >= (model.mins[4]))
model.cons_sup4 = pe.Constraint(expr=(model.mins[4]) >= (model.mins[5]))
model.cons_sup5 = pe.Constraint(expr=(model.mins[5]) >= (model.mins[6]))
model.cons_sup6 = pe.Constraint(expr=(model.mins[6]) >= (model.mins[7]))
model.cons_sup7 = pe.Constraint(expr=(model.mins[7]) >= (model.mins[8]))
model.cons_sup8 = pe.Constraint(expr=(model.mins[8]) >= (model.mins[9]))
model.cons_sup9 = pe.Constraint(expr=(model.mins[9]) >= (model.mins[10]))
model.cons_sup10 = pe.Constraint(expr=(model.mins[10]) >= (model.mins[11]))
model.cons_sup11 = pe.Constraint(expr=(model.mins[11]) >= (model.mins[12]))
model.cons_sup12 = pe.Constraint(expr=(model.mins[12]) >= (model.mins[13]))
model.cons_sup13 = pe.Constraint(expr=(model.mins[13]) >= (model.mins[14]))

# Michael Porter Jr Bonus Linking Constraint
model.cons_MPJ = pe.Constraint(expr=(model.binMPJ*15) >= (model.mins[13]))

#OBJECTIVE Function
model.obj = pe.Objective(expr=sum(model.mins[i]*data.iloc[i,0] for i in decision_index) + sum(model.bin5[i]*1 for i in decision_index) + sum(model.bin15[i]*1 for i in decision_index) + (model.binMPJ*3) , sense=-1)

model.pprint()


# ##### [Back to Top](#Top)

# # 4. Model Solution<a id=4></a>

# In[61]:




#Solve Model
opt = pe.SolverFactory('glpk')
success = opt.solve(model, tee=False)

#Display Results the following table indicates

print(f'objective value is {model.obj.expr()}')
rotation =  pd.DataFrame(model.mins[i].value for i in decision_index)
rotation.index = raw_data.iloc[6:21, 2]
rotation.columns = [ 'assigned minutes per game']
rotation


# ##### [Back to Top](#Top)

# # 5. Sensitivity Analysis<a id=5></a>

# ## 5.1 Sensitivity Analysis Make Michael Porter Jr.'s Adj. RPM 0 <a id=5></a>
# This will simulate the rotation when the currently underpreforming but high potential Michael Porter Jr. develops his game to be a standard where his effect is neither positive or negative

# First Import New Data Where MPJ's Adj RMP is 0 and his posiotionality reflects this change

# In[70]:



raw_data_mpj = pd.read_excel('FinalData.xlsx', sheet_name='MPJ')
raw_data_mpj


# Now Update The Model

# In[71]:


data_mpj = pd.DataFrame(raw_data_mpj.iloc[6:21, 5])
data_mpj.columns = ['Adj. RPM']
data_mpj.index = raw_data_mpj.iloc[6:21, 2]
# note players arw pre-sorted by minutes adjusted Real Plus Minus
data_mpj

# Craete Pyomo Model and Build It Objective and Comstraints
model = pe.ConcreteModel()
decision_index = range(15)

model.mins = pe.Var(decision_index, domain=pe.Integers, bounds=(0,36))
model.bin5 = pe.Var(decision_index, domain=pe.Binary)
model.bin15 = pe.Var(decision_index, domain=pe.Binary)
model.binMPJ = pe.Var(domain=pe.Binary)


#CONSTRAINTS

# Total Mins Played == 240
model.tot_mins = pe.Constraint(expr=sum(model.mins[i] for i in decision_index) == 240)
    
# constraints that force a player to play over 5 mins per game if they get the over 5 min bonus
model.cons_five_0 = pe.Constraint(expr=(model.bin5[0]*5) <= (model.mins[0]))
model.cons_five_1 = pe.Constraint(expr=(model.bin5[1]*5) <= (model.mins[1]))
model.cons_five_2 = pe.Constraint(expr=(model.bin5[2]*5) <= (model.mins[2]))
model.cons_five_3 = pe.Constraint(expr=(model.bin5[3]*5) <= (model.mins[3]))
model.cons_five_4 = pe.Constraint(expr=(model.bin5[4]*5) <= (model.mins[4]))
model.cons_five_5 = pe.Constraint(expr=(model.bin5[5]*5) <= (model.mins[5]))
model.cons_five_6 = pe.Constraint(expr=(model.bin5[6]*5) <= (model.mins[6]))
model.cons_five_7 = pe.Constraint(expr=(model.bin5[7]*5) <= (model.mins[7]))
model.cons_five_8 = pe.Constraint(expr=(model.bin5[8]*5) <= (model.mins[8]))
model.cons_five_9 = pe.Constraint(expr=(model.bin5[9]*5) <= (model.mins[9]))
model.cons_five_10 = pe.Constraint(expr=(model.bin5[10]*5) <= (model.mins[10]))
model.cons_five_11 = pe.Constraint(expr=(model.bin5[11]*5) <= (model.mins[11]))
model.cons_five_12 = pe.Constraint(expr=(model.bin5[12]*5) <= (model.mins[12]))
model.cons_five_13 = pe.Constraint(expr=(model.bin5[13]*5) <= (model.mins[13]))
model.cons_five_14 = pe.Constraint(expr=(model.bin5[14]*5) <= (model.mins[14]))

# constraints that force a player to play over 15 mins per game if they get the over 15 min bonus
model.cons_fifteen_0 = pe.Constraint(expr=(model.bin15[0]*15) <= (model.mins[0]))
model.cons_fifteen_1 = pe.Constraint(expr=(model.bin15[1]*15) <= (model.mins[1]))
model.cons_fifteen_2 = pe.Constraint(expr=(model.bin15[2]*15) <= (model.mins[2]))
model.cons_fifteen_3 = pe.Constraint(expr=(model.bin15[3]*15) <= (model.mins[3]))
model.cons_fifteen_4 = pe.Constraint(expr=(model.bin15[4]*15) <= (model.mins[4]))
model.cons_fifteen_5 = pe.Constraint(expr=(model.bin15[5]*15) <= (model.mins[5]))
model.cons_fifteen_6 = pe.Constraint(expr=(model.bin15[6]*15) <= (model.mins[6]))
model.cons_fifteen_7 = pe.Constraint(expr=(model.bin15[7]*15) <= (model.mins[7]))
model.cons_fifteen_8 = pe.Constraint(expr=(model.bin15[8]*15) <= (model.mins[8]))
model.cons_fifteen_9 = pe.Constraint(expr=(model.bin15[9]*15) <= (model.mins[9]))
model.cons_fifteen_10 = pe.Constraint(expr=(model.bin15[10]*15) <= (model.mins[10]))
model.cons_fifteen_11 = pe.Constraint(expr=(model.bin15[11]*15) <= (model.mins[11]))
model.cons_fifteen_12 = pe.Constraint(expr=(model.bin15[12]*15) <= (model.mins[12]))
model.cons_fifteen_13 = pe.Constraint(expr=(model.bin15[13]*15) <= (model.mins[13]))
model.cons_fifteen_14 = pe.Constraint(expr=(model.bin15[14]*15) <= (model.mins[14]))

# constraints that force players with higher Adj Real Plus Minus to play more
model.cons_sup0 = pe.Constraint(expr=(model.mins[0]) >= (model.mins[1]))
model.cons_sup1 = pe.Constraint(expr=(model.mins[1]) >= (model.mins[2]))
model.cons_sup2 = pe.Constraint(expr=(model.mins[2]) >= (model.mins[3]))
model.cons_sup3 = pe.Constraint(expr=(model.mins[3]) >= (model.mins[4]))
model.cons_sup4 = pe.Constraint(expr=(model.mins[4]) >= (model.mins[5]))
model.cons_sup5 = pe.Constraint(expr=(model.mins[5]) >= (model.mins[6]))
model.cons_sup6 = pe.Constraint(expr=(model.mins[6]) >= (model.mins[7]))
model.cons_sup7 = pe.Constraint(expr=(model.mins[7]) >= (model.mins[8]))
model.cons_sup8 = pe.Constraint(expr=(model.mins[8]) >= (model.mins[9]))
model.cons_sup9 = pe.Constraint(expr=(model.mins[9]) >= (model.mins[10]))
model.cons_sup10 = pe.Constraint(expr=(model.mins[10]) >= (model.mins[11]))
model.cons_sup11 = pe.Constraint(expr=(model.mins[11]) >= (model.mins[12]))
model.cons_sup12 = pe.Constraint(expr=(model.mins[12]) >= (model.mins[13]))
model.cons_sup13 = pe.Constraint(expr=(model.mins[13]) >= (model.mins[14]))

# Michael Porter Jr Bonus Linking Constraint
model.cons_MPJ = pe.Constraint(expr=(model.binMPJ*15) >= (model.mins[5]))

#OBJECTIVE Function
model.obj = pe.Objective(expr=sum(model.mins[i]*data_mpj.iloc[i,0] for i in decision_index) + sum(model.bin5[i]*1 for i in decision_index) + sum(model.bin15[i]*1 for i in decision_index) + (model.binMPJ*3) , sense=-1)

model.pprint()


# In[73]:



#Solve New Model
opt = pe.SolverFactory('glpk')
success = opt.solve(model, tee=False)

#Display Results the following table indicates

print(f'objective value is {model.obj.expr()}')
rotation_1 =  pd.DataFrame(model.mins[i].value for i in decision_index)
rotation_1.index = raw_data_mpj.iloc[6:21, 2]
rotation_1.columns = [ 'assigned minutes per game']
rotation_1


# In[ ]:





# ## 5.2 The point bonus for having a player play 15 minutes per game is removed
# the coaching staff decides that playing a comparitively bad play for 15 minutes is unnessacary and decides thatt the 5 minute point bonus is sufficient to mainatain team morale

# Update The model, specifically update the objective function

# In[65]:


# Craete Pyomo Model and Build It Objective and Comstraints
model = pe.ConcreteModel()
decision_index = range(15)

model.mins = pe.Var(decision_index, domain=pe.Integers, bounds=(0,36))
model.bin5 = pe.Var(decision_index, domain=pe.Binary)
model.bin15 = pe.Var(decision_index, domain=pe.Binary)
model.binMPJ = pe.Var(domain=pe.Binary)


#CONSTRAINTS

# Total Mins Played == 240
model.tot_mins = pe.Constraint(expr=sum(model.mins[i] for i in decision_index) == 240)
    
# constraints that force a player to play over 5 mins per game if they get the over 5 min bonus
model.cons_five_0 = pe.Constraint(expr=(model.bin5[0]*5) <= (model.mins[0]))
model.cons_five_1 = pe.Constraint(expr=(model.bin5[1]*5) <= (model.mins[1]))
model.cons_five_2 = pe.Constraint(expr=(model.bin5[2]*5) <= (model.mins[2]))
model.cons_five_3 = pe.Constraint(expr=(model.bin5[3]*5) <= (model.mins[3]))
model.cons_five_4 = pe.Constraint(expr=(model.bin5[4]*5) <= (model.mins[4]))
model.cons_five_5 = pe.Constraint(expr=(model.bin5[5]*5) <= (model.mins[5]))
model.cons_five_6 = pe.Constraint(expr=(model.bin5[6]*5) <= (model.mins[6]))
model.cons_five_7 = pe.Constraint(expr=(model.bin5[7]*5) <= (model.mins[7]))
model.cons_five_8 = pe.Constraint(expr=(model.bin5[8]*5) <= (model.mins[8]))
model.cons_five_9 = pe.Constraint(expr=(model.bin5[9]*5) <= (model.mins[9]))
model.cons_five_10 = pe.Constraint(expr=(model.bin5[10]*5) <= (model.mins[10]))
model.cons_five_11 = pe.Constraint(expr=(model.bin5[11]*5) <= (model.mins[11]))
model.cons_five_12 = pe.Constraint(expr=(model.bin5[12]*5) <= (model.mins[12]))
model.cons_five_13 = pe.Constraint(expr=(model.bin5[13]*5) <= (model.mins[13]))
model.cons_five_14 = pe.Constraint(expr=(model.bin5[14]*5) <= (model.mins[14]))

# constraints that force a player to play over 15 mins per game if they get the over 15 min bonus
model.cons_fifteen_0 = pe.Constraint(expr=(model.bin15[0]*15) <= (model.mins[0]))
model.cons_fifteen_1 = pe.Constraint(expr=(model.bin15[1]*15) <= (model.mins[1]))
model.cons_fifteen_2 = pe.Constraint(expr=(model.bin15[2]*15) <= (model.mins[2]))
model.cons_fifteen_3 = pe.Constraint(expr=(model.bin15[3]*15) <= (model.mins[3]))
model.cons_fifteen_4 = pe.Constraint(expr=(model.bin15[4]*15) <= (model.mins[4]))
model.cons_fifteen_5 = pe.Constraint(expr=(model.bin15[5]*15) <= (model.mins[5]))
model.cons_fifteen_6 = pe.Constraint(expr=(model.bin15[6]*15) <= (model.mins[6]))
model.cons_fifteen_7 = pe.Constraint(expr=(model.bin15[7]*15) <= (model.mins[7]))
model.cons_fifteen_8 = pe.Constraint(expr=(model.bin15[8]*15) <= (model.mins[8]))
model.cons_fifteen_9 = pe.Constraint(expr=(model.bin15[9]*15) <= (model.mins[9]))
model.cons_fifteen_10 = pe.Constraint(expr=(model.bin15[10]*15) <= (model.mins[10]))
model.cons_fifteen_11 = pe.Constraint(expr=(model.bin15[11]*15) <= (model.mins[11]))
model.cons_fifteen_12 = pe.Constraint(expr=(model.bin15[12]*15) <= (model.mins[12]))
model.cons_fifteen_13 = pe.Constraint(expr=(model.bin15[13]*15) <= (model.mins[13]))
model.cons_fifteen_14 = pe.Constraint(expr=(model.bin15[14]*15) <= (model.mins[14]))

# constraints that force players with higher Adj Real Plus Minus to play more
model.cons_sup0 = pe.Constraint(expr=(model.mins[0]) >= (model.mins[1]))
model.cons_sup1 = pe.Constraint(expr=(model.mins[1]) >= (model.mins[2]))
model.cons_sup2 = pe.Constraint(expr=(model.mins[2]) >= (model.mins[3]))
model.cons_sup3 = pe.Constraint(expr=(model.mins[3]) >= (model.mins[4]))
model.cons_sup4 = pe.Constraint(expr=(model.mins[4]) >= (model.mins[5]))
model.cons_sup5 = pe.Constraint(expr=(model.mins[5]) >= (model.mins[6]))
model.cons_sup6 = pe.Constraint(expr=(model.mins[6]) >= (model.mins[7]))
model.cons_sup7 = pe.Constraint(expr=(model.mins[7]) >= (model.mins[8]))
model.cons_sup8 = pe.Constraint(expr=(model.mins[8]) >= (model.mins[9]))
model.cons_sup9 = pe.Constraint(expr=(model.mins[9]) >= (model.mins[10]))
model.cons_sup10 = pe.Constraint(expr=(model.mins[10]) >= (model.mins[11]))
model.cons_sup11 = pe.Constraint(expr=(model.mins[11]) >= (model.mins[12]))
model.cons_sup12 = pe.Constraint(expr=(model.mins[12]) >= (model.mins[13]))
model.cons_sup13 = pe.Constraint(expr=(model.mins[13]) >= (model.mins[14]))

# Michael Porter Jr Bonus Linking Constraint
model.cons_MPJ = pe.Constraint(expr=(model.binMPJ*15) >= (model.mins[13]))

#OBJECTIVE Function
model.obj = pe.Objective(expr=sum(model.mins[i]*data.iloc[i,0] for i in decision_index) + sum(model.bin5[i]*1 for i in decision_index) + (model.binMPJ*3) , sense=-1)

model.pprint()


# In[66]:


#Solve new Model
opt = pe.SolverFactory('glpk')
success = opt.solve(model, tee=False)

#Display Results the following table indicates

print(f'objective value is {model.obj.expr()}')
rotation_2 =  pd.DataFrame(model.mins[i].value for i in decision_index)
rotation_2.index = raw_data.iloc[6:21, 2]
rotation_2.columns = [ 'assigned minutes per game']
rotation_2


# ## 5.3 The Maximum a player can play is raised to 40 minutes
# this reflects a possible change if squad fitness goes up or a rotation will be built for the players were short term results supercede long term player fitness

# Update the model, specifically update mins to ahve an upper bound of 40 not 36

# In[74]:


# Craete Pyomo Model and Build It Objective and Comstraints
model = pe.ConcreteModel()
decision_index = range(15)
#Updated Bounds
model.mins = pe.Var(decision_index, domain=pe.Integers, bounds=(0,40))
model.bin5 = pe.Var(decision_index, domain=pe.Binary)
model.bin15 = pe.Var(decision_index, domain=pe.Binary)
model.binMPJ = pe.Var(domain=pe.Binary)


#CONSTRAINTS

# Total Mins Played == 240
model.tot_mins = pe.Constraint(expr=sum(model.mins[i] for i in decision_index) == 240)
    
# constraints that force a player to play over 5 mins per game if they get the over 5 min bonus
model.cons_five_0 = pe.Constraint(expr=(model.bin5[0]*5) <= (model.mins[0]))
model.cons_five_1 = pe.Constraint(expr=(model.bin5[1]*5) <= (model.mins[1]))
model.cons_five_2 = pe.Constraint(expr=(model.bin5[2]*5) <= (model.mins[2]))
model.cons_five_3 = pe.Constraint(expr=(model.bin5[3]*5) <= (model.mins[3]))
model.cons_five_4 = pe.Constraint(expr=(model.bin5[4]*5) <= (model.mins[4]))
model.cons_five_5 = pe.Constraint(expr=(model.bin5[5]*5) <= (model.mins[5]))
model.cons_five_6 = pe.Constraint(expr=(model.bin5[6]*5) <= (model.mins[6]))
model.cons_five_7 = pe.Constraint(expr=(model.bin5[7]*5) <= (model.mins[7]))
model.cons_five_8 = pe.Constraint(expr=(model.bin5[8]*5) <= (model.mins[8]))
model.cons_five_9 = pe.Constraint(expr=(model.bin5[9]*5) <= (model.mins[9]))
model.cons_five_10 = pe.Constraint(expr=(model.bin5[10]*5) <= (model.mins[10]))
model.cons_five_11 = pe.Constraint(expr=(model.bin5[11]*5) <= (model.mins[11]))
model.cons_five_12 = pe.Constraint(expr=(model.bin5[12]*5) <= (model.mins[12]))
model.cons_five_13 = pe.Constraint(expr=(model.bin5[13]*5) <= (model.mins[13]))
model.cons_five_14 = pe.Constraint(expr=(model.bin5[14]*5) <= (model.mins[14]))

# constraints that force a player to play over 15 mins per game if they get the over 15 min bonus
model.cons_fifteen_0 = pe.Constraint(expr=(model.bin15[0]*15) <= (model.mins[0]))
model.cons_fifteen_1 = pe.Constraint(expr=(model.bin15[1]*15) <= (model.mins[1]))
model.cons_fifteen_2 = pe.Constraint(expr=(model.bin15[2]*15) <= (model.mins[2]))
model.cons_fifteen_3 = pe.Constraint(expr=(model.bin15[3]*15) <= (model.mins[3]))
model.cons_fifteen_4 = pe.Constraint(expr=(model.bin15[4]*15) <= (model.mins[4]))
model.cons_fifteen_5 = pe.Constraint(expr=(model.bin15[5]*15) <= (model.mins[5]))
model.cons_fifteen_6 = pe.Constraint(expr=(model.bin15[6]*15) <= (model.mins[6]))
model.cons_fifteen_7 = pe.Constraint(expr=(model.bin15[7]*15) <= (model.mins[7]))
model.cons_fifteen_8 = pe.Constraint(expr=(model.bin15[8]*15) <= (model.mins[8]))
model.cons_fifteen_9 = pe.Constraint(expr=(model.bin5[9]*15) <= (model.mins[9]))
model.cons_fifteen_10 = pe.Constraint(expr=(model.bin15[10]*15) <= (model.mins[10]))
model.cons_fifteen_11 = pe.Constraint(expr=(model.bin15[11]*15) <= (model.mins[11]))
model.cons_fifteen_12 = pe.Constraint(expr=(model.bin15[12]*15) <= (model.mins[12]))
model.cons_fifteen_13 = pe.Constraint(expr=(model.bin15[13]*15) <= (model.mins[13]))
model.cons_fifteen_14 = pe.Constraint(expr=(model.bin15[14]*15) <= (model.mins[14]))

# constraints that force players with higher Adj Real Plus Minus to play more
model.cons_sup0 = pe.Constraint(expr=(model.mins[0]) >= (model.mins[1]))
model.cons_sup1 = pe.Constraint(expr=(model.mins[1]) >= (model.mins[2]))
model.cons_sup2 = pe.Constraint(expr=(model.mins[2]) >= (model.mins[3]))
model.cons_sup3 = pe.Constraint(expr=(model.mins[3]) >= (model.mins[4]))
model.cons_sup4 = pe.Constraint(expr=(model.mins[4]) >= (model.mins[5]))
model.cons_sup5 = pe.Constraint(expr=(model.mins[5]) >= (model.mins[6]))
model.cons_sup6 = pe.Constraint(expr=(model.mins[6]) >= (model.mins[7]))
model.cons_sup7 = pe.Constraint(expr=(model.mins[7]) >= (model.mins[8]))
model.cons_sup8 = pe.Constraint(expr=(model.mins[8]) >= (model.mins[9]))
model.cons_sup9 = pe.Constraint(expr=(model.mins[9]) >= (model.mins[10]))
model.cons_sup10 = pe.Constraint(expr=(model.mins[10]) >= (model.mins[11]))
model.cons_sup11 = pe.Constraint(expr=(model.mins[11]) >= (model.mins[12]))
model.cons_sup12 = pe.Constraint(expr=(model.mins[12]) >= (model.mins[13]))
model.cons_sup13 = pe.Constraint(expr=(model.mins[13]) >= (model.mins[14]))

# Michael Porter Jr Bonus Linking Constraint
model.cons_MPJ = pe.Constraint(expr=(model.binMPJ*15) >= (model.mins[13]))

#OBJECTIVE Function
model.obj = pe.Objective(expr=sum(model.mins[i]*data.iloc[i,0] for i in decision_index) + sum(model.bin5[i]*1 for i in decision_index) + sum(model.bin15[i]*1 for i in decision_index) + (model.binMPJ*3) , sense=-1)

model.pprint()


# In[75]:




#Solve Model
opt = pe.SolverFactory('glpk')
success = opt.solve(model, tee=False)

#Display Results the following table indicates

print(f'objective value is {model.obj.expr()}')
rotation_3 =  pd.DataFrame(model.mins[i].value for i in decision_index)
rotation_3.index = raw_data.iloc[6:21, 2]
rotation_3.columns = [ 'assigned minutes per game']
rotation_3


# ##### [Back to Top](#Top)

# # 6. Conclusions<a id=6></a>

# ## 6.1 Tactical Information<a id=6.1></a>

# Based on the current model and value judgements made in the model the rotation should look as follows

# In[76]:


rotation


# ## 6.2 Strategic Information<a id=6.2></a>

# Strategic Information from 5.1: If we focused on the development of Michael Porter Jr. we would have increased from 20.3 to 30.9 some of that would be from him getting the 15 minute per game 1 point bonus, but the rest would have been from increased conribution on the court. In addition, him playing more would certainly aid his longer-term development. This advantage is not seen in our model as the threshold for a point bonus for Michael Porter Jr. playing more was set at 20 minutes per game, a threshold which the updated model does not meet. This withstanding, it may be more efficent to focus on the development of already higher performing players. To truly understand this dynamic, more research must be done to understand which players would benefit most from more concentration on their development in terms of increased RPM. In addition (specifically with regards to Michael Porter Jr.), more research must be done on how his gametime will impact his long term development. 
#     
# Stretegic Information from 5.2: If the coaching staff finds that most lower performing players playing less time will have no or little effect on team morale then this than we should allow this as then we will be able to put our better players on the court for longer. To do this we need research investigating how this would effect team morale, and then how this team morale would effect on court play so that we could integrate this into our model by determining what 
# 
# Strategic Information from 5.3: There would be a .7 increase in the objective function if this change were in place. In additon since Jokic would be the only player playing over the 36 minute minimum, we could simply focus on Jokic's fitness instead of deveoting resources for the whole team to have increased fitness

# ##### [Back to Top](#Top)

# # 7. Model Limitations, Future Improvements and Challenges<a id=7></a>

# # LIMITATIONS
# 
# Firstly, Many of the models assumptions and conditions are based on vague and/or arbituary notions without any real basis to support it. For example, mnay of the models' constraints are based off of perserving team morale, avague notion in and of itself. At current, we have a set of constraints that must be satisied that are based on morale. This creates a binary model of either having 'good' or 'bad/unacceptable' morale, however this is not repersentative of morale being non-discrete.
# 
# In addition we make assumptions and arbituary decisons such as Micahel Porter Jr. getting a boost in consideration of the aid this will have to his development when he plays 20 minutes or more but no boost if he plays 19. This does not make much sense, so we should have a better understanding of the value of the marginal benefit of him playing each aditional minute on a non-binary scale, so that the model can reflect this better.
# 
# Finally, this model does not say when each player should be on the court, thus it cannot account for the vunrebilities of having a certain combination of players on the court at once that individually may be good, but together have ceratain vunrebilites as a collective that need to be addressed.
# 
# # FUTURE Improvements
# 
# I see two iterations of future improvements:
# 
# First iteration:
# - move to ipopt (nonlinear model) to be able to accomodate the following changes
# - measure team morale quanatively on a non-discrete scale as a function of the perviously discussed factors and uses that team morale to adjust on court performance (the objective function)
# - have a better account of the effect playing time of each of player has on their long term development and how that development will help the team moving forward. Intragate that calculation into the objective function to account for long term devlopment more broadly than just considering MPJ
# 
# Second Iteration:
# - move to an eveolutionary solver (though I don't know which one that is in pyomo)
# - consider not only how much time a player is playing but which combination of players will be on the floor at once. Then we will be able to address and account for vurebilites a collective will have that can be exploited by an oppentent such as (being too short, being too offensively/defensively orientated, or not having a player capabe of being a primary ball handler). 

# ##### [Back to Top](#Top)
