# RL-Adversarial-Agents--Tag
Reinforcement learning model for two competing agents to learn to play tag. 
Specifically applies methods to limit state-space size for large environments with three levels of abstraction.
The first being a 3X3 grid centered around each agent that gives them information about their immediate surroundings.
Next, a quadrant map is used to tell each agent the general location of their target, wether they are above/below and left/right.
Finally, a time series decoupling is used to separate repeated states in the same game. Or rather if a state is experienced more than once in a single game
each new experience will be treated as a new state in the Q table. This is done by adding a time modifier to the end of every state encoding. Lastly, note that this
time modifier is mod 200 and so will allow for repeated states if any particular state is re-experienced more than 200 times in a single game.

## Table of contents for the file.
This section includes a brief description of each file in the project.
> game.py handles environment information about the game boards. Including creating new random environment and move
    game characters.

> object.py is a class file that holds information for every type of non-playable objet including walls and empty space.

> agent.py is a class file that holds information about every type of AI agent that can be trained in the model. This 
includes seekers, runners, and fixed goals. This file maintains all functions related to agents including managing q-tables
and distinct reward functions. Along with environment encoding.

> Qtable.py is a helper class for agent and stores a look-up dictionary of all Q states experienced so far and their associated Q value
for each state action pair. Also includes methods for updating Q values with bellman updates. algorithm hyperparameters, gamma and alpha can
be found in this method in the update Q-table function.

> util.py contains an implementation of a limited depth quad tree that can be used to further encode the surroundings of each agent. Or rather to encode the entire
game board in some uncertain model. This however is not used in the project because any additional benefit seen by adding a limited depth tree also resulted in the overall state
space becoming to large to fit into the scope of the report. (which is to facilitate learning while using the smallest possible Q table.)

> GUI.py controls functions for displaying the game.

> demo.py is going to be used to showcase the pre-trained agents abilities on game boards of different types and sizes. More instructions on this are provided further down.

> game_instance.py runs a single game instance and allows all agents to play until a stopping criteria is reached. Returns information about the final status of the game at completion.

> lean.py is the primary training function for the RL model. And so is used to train new agents. Note, some agents have already been pre-trained and pickled, and so are ready to 
be demoed without re-training. However, a description of how to train new agents is included further down.

## Demoing pre-trained agents.
Training take a long time and so I think one of the best ways to showcase the project is to give the option to load pre-trained agents into different environments.
This also demonstrates the adaptive policies of the agents.
> In general, demo.py take terminal options to load different agents and different game board types.

> First run python demo.py this will select default seeker.pkl and runner.pkl and a random game board.
```
python demo.py
```

From here you can change the inputs to the terminal command. First select a better agent with

```
python demo.py --SFile Seeker_Basic_Tree.pkl --RFile Runner_Basic_Tree.pkl
```

This will load the agents trained will all three levels of state space abstraction.
>From here you can change the type of the game board by using,

```
python demo.py --SFile Seeker_Basic_Tree.pkl --RFile Runner_Basic_Tree.pkl -z 25
```
change 25 to any integer.

>Next, you can change the amount of games are run in the demo.
```
python demo.py --SFile Seeker_Basic_Tree.pkl --RFile Runner_Basic_Tree.pkl -z 25 -n 5
```

> You can also change the type of game environment to something more principled.

```
python demo.py --SFile Seeker_Basic_Tree.pkl --RFile Runner_Basic_Tree.pkl -z 25 -n 5 -t roomsGrid
```
Other options for game environments are, ['roomsGrid' , 'randomGrid', 'uniformGrid', 'emptyGrid'] select any of to showcase.

> I think this completes the useful parameters that can be changed in the demo.py file. From here it may be fun to put the
different agents against each other. Try switching the --SFile or --RFile to some of the following.
--SFile  -> [Seeker_Basic_Tree.pkl , Seeker.pkl]
--RFile  -> [Runner_Basic_Tree.pkl , Runner.pkl]


## Training new agents
> This section leads through how to train new agents. There are only a few easy commands from the terminal.
In general training can take a long time, however, the the algorithm will demo the agents progress every 1000
or so games (which is about every 2 minutes) and so I recommend starting a training cycle then canceling the run
after a few thousand epocs.

```
python learn.py
```
This command runs the  default learning curriculum that puts two agents equipped with all three levels of state abstraction against
each other. In general, this is a very short learning cycle, about 15 thousand epocs in total that will train 5000 epocs on each 
type of environment ['roomsGrid' , 'randomGrid', 'uniformGrid'].
This training function is not used when training the pre-trained models. However, something similar is used just expanded to 100k epocs,
which takes about 90 minutes in total to train. In contrast this default curriculum usually takes about 10 minutes to finish training.
> This training function will automatically pickle the agents to files,
'Default_Seeker.pkl' and 'Default_Runner.pkl' which can then be demoed again with,
```
python demo.py --SFile Default_Seeker.pkl --RFile Default_Runner.pkl
```
The above sections provide a instructions for a high level showcase of the project. From here, most files have their own test cases that can be run;
however, I don't think it will be that interesting. Most of the fun algorithm specific code is in game_instance.py, agent.py, and Qtable.py.




