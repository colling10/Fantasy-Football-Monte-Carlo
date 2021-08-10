# Fantasy-Football-Monte-Carlo

This code is to find the probability of what place each team will finish at the end of the fantasy football regular season. This is done by looping through n number of simulated seasons, adding 1 to each team's placements at the end of the season, and then finally dividing each team's number of placements by n. The simulated scores are created by randomly selecting values from everyone's normal distribution, which were created from everyone's average score and standard deviation of the real scores so far. 

There is an input txt file to enter the schedule and scores so far, and an output txt file with the probabilities. 
This is my first "big" project with python, so the the input txt file must be formatted correctly with no leniency on mispellings. 
Happy to hear comments or feedback. Example of required formatting can be found in the input txt file.
