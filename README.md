# RL-Adversarial-Agents--Tag  

- Reinforcement learning model for two competing agents to learn to play tag.  
- Specifically applies methods to limit state-space size for large environments with three levels of abstraction.  
- The first being a 3X3 grid centered around each agent that gives them information about their immediate surroundings.  
- Next, a quadrant map is used to tell each agent the general location of their target, wether they are above/below and left/right.  
- A time series decoupling is used to separate repeated states in the same game. Or rather if a state is experienced more than once in a single game
each new experience will be treated as a new state in the Q table. This is done by adding a time modifier to the end of every state encoding.
- Note that this time modifier is mod 200 and so will allow for repeated states if any particular state is re-experienced more than 200 times in a single game.  

## Summary

Reinforcement learning is a common technique in the development of intelligent agents. In particular, many
agents can take information about their surroundings to learn complex tasks such as playing chess or navi-
gating distressed environments. However, as these tasks become more complicated it may become relevant
to preferentially select informational attributes of the environment that most help in the learning process. For
example, if an agent is given to much information is may be unable to discern what is important to completing
the task, while if given to little information, the agent may miss something critical. Within the scope of this
report, we examine state space reduction techniques that limit the amount of information an agent receives
from its environment to improve learning speed. Fundamentally this utilizes a discrete Q-learning algorithm
to manage policy generation over time. Our experiment is to design adversarial agents to compete in a game
of tag over a randomly generated environment. The randomness of the game environment makes it more
difficult for the agents to learn adaptive search and/or evade policies and highlights the effectiveness of our
state space reduction technique.  

## Design

Two agents are designed to compete in a game of tag. The game is played on a rectangular grid where each game object
can occupy a single space. Aside from the agents, there are walls that block movement. In general agent 1 (seeker) is
tasked with seeking out agent 2 (runner) and occupying that same space. This results in agent 1 winning the game and
getting a reward and agent 2 losing reward. Additionally, if agent 2 survives 200 game steps the game ends. This will
evolve two learning policies for the different agents that are optimized in competition with each other. After each game,
a new random environment is created and the agents are allowed to play again. This continues for 100, 000 epocs. The
randomness contributes to adaptive policies and allows for the agents to be placed in any environment and still preform
fairly well in terms of meeting their distinct objectives. And as a consequence of this, after training the agents are placed
in very complex more principally generated terrains to test the strength of their policies.

## Table Of Contents

This section includes a brief description of each file in the project.

- Video_Demo
  - Folder containing DIFs with visual results (view to watch the results of the pre-trained models)
  - Video_Demo/Abstraction_lvl_1_2_3.GIF is the result of the complete state space.  

- src
  - Folder containing all code

- src/Q_tables
  - Storage folder to hold pre-trained Q tables.

- src/game.py  
  - handles environment information about the game boards. Including creating new random environment and move game characters.  

- src/object.py  
  - is a class file that holds information for every type of non-playable objet including walls and empty space.  

- src/agent.py  
  - A class file that holds information about every type of AI agent that can be trained in the model.  
  - This includes seekers, runners, and fixed goals.  
  - This file maintains all functions related to agents including managing q-tables
    and distinct reward functions. Along with environment encoding.

- src/Qtable.py  
  - A helper class for agent and stores a look-up dictionary of all Q states experienced so far and their associated Q value
    for each state action pair.  
  - Also includes methods for updating Q values with bellman updates. algorithm hyperparameters, gamma and alpha can
    be found in this method in the update Q-table function.

- src/util.py  
  - contains an implementation of a limited depth quad tree that can be used to further encode the surroundings of each agent. Or rather to encode the entire
    game board in some uncertain model.  
  - This however is not used in the project because any additional benefit seen by adding a limited depth tree also resulted in the overall state
    space becoming to large to fit into the scope of the report. (which is to facilitate learning while using the smallest possible Q table.)

- src/GUI.py  
  - controls functions for displaying the game.

- src/demo.py  
  - is going to be used to showcase the pre-trained agents abilities on game boards of different types and sizes.  
  - More instructions on this are provided further down.

- src/game_instance.py  
  - runs a single game instance and allows all agents to play until a stopping criteria is reached.  
  - Returns information about the final status of the game at completion.

- src/lean.py  
  - The primary training function for the RL model.  
  - And so is used to train new agents.  
  - Note, some agents have already been pre-trained and pickled, and so are ready to be demoed without re-training.  
  - A description of how to train new agents is included further down.

## Demoing pre-trained agents

Training take a long time and so I think one of the best ways to showcase the project is to give the option to load pre-trained agents into different environments.
This also demonstrates the adaptive policies of the agents.

- In general, demo.py take terminal options to load different agents and different game board types.  

cd into the src folder,  

```console
cd src
```

- Run python demo.py this will select default seeker.pkl and runner.pkl and a random game board.

```console
python demo.py
```

From here you can change the inputs to the terminal command. First select a better agent with

```console
python demo.py --SFile Q_tables/Seeker_Basic_Tree.pkl --RFile Q_tables/Runner_Basic_Tree.pkl
```

This will load the agents trained will all three levels of state space abstraction.  

- From here you can change the type of the game board by using,

```console
python demo.py --SFile Q_tables/Seeker_Basic_Tree.pkl --RFile Q_tables/Runner_Basic_Tree.pkl -z 25
```

change 25 to any integer.

- Next, you can change the amount of games are run in the demo.

```console
python demo.py --SFile Q_tables/Seeker_Basic_Tree.pkl --RFile Q_tables/Runner_Basic_Tree.pkl -z 25 -n 5
```

- You can also change the type of game environment to something more principled.

```console
python demo.py --SFile Q_tables/Seeker_Basic_Tree.pkl --RFile Q_tables/Runner_Basic_Tree.pkl -z 25 -n 5 -t roomsGrid
```

Other options for game environments are, ['roomsGrid' , 'randomGrid', 'uniformGrid', 'emptyGrid'] select any of to showcase.

- I think this completes the useful parameters that can be changed in the demo.py file. From here it may be fun to put the
different agents against each other. Try switching the --SFile or --RFile to some of the following.  
--SFile  -> [Q_tables/Seeker_Basic_Tree.pkl , Q_tables/Seeker.pkl]  
--RFile  -> [Q_tables/Runner_Basic_Tree.pkl , Q_tables/Runner.pkl]  

## Training new agents

cd into the src folder,  

```console
cd src
```

- This section leads through how to train new agents. There are only a few easy commands from the terminal.
In general training can take a long time, however, the the algorithm will demo the agents progress every 1000
or so games (which is about every 2 minutes) and so I recommend starting a training cycle then canceling the run
after a few thousand epocs.

```console
python learn.py
```

This command runs the  default learning curriculum that puts two agents equipped with all three levels of state abstraction against
each other. In general, this is a very short learning cycle, about 15 thousand epocs in total that will train 5000 epocs on each
type of environment ['roomsGrid' , 'randomGrid', 'uniformGrid'].
This training function is not used when training the pre-trained models. However, something similar is used just expanded to 100k epocs,
which takes about 90 minutes in total to train. In contrast this default curriculum usually takes about 10 minutes to finish training.

- This training function will automatically pickle the agents to files,
'Default_Seeker.pkl' and 'Default_Runner.pkl' which can then be demoed again with,

```console
python demo.py --SFile Q_tables/Default_Seeker.pkl --RFile Q_tables/Default_Runner.pkl
```

The above sections provide a instructions for a high level showcase of the project. From here, most files have their own test cases that can be run;
however, I don't think it will be that interesting. Most of the fun algorithm specific code is in game_instance.py, agent.py, and Qtable.py.
