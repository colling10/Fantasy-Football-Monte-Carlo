#get your libraries
import re
import random
import math
from statistics import NormalDist

#make some math shit, could import from statistics,
#but wanted to try making my own function. Potential error source
def mean(data):
    n = len(data)
    mean = sum(data) / n
    return mean

def variance(data):
    n = len(data)
    mean = sum(data) / n
    deviations = [(x - mean) ** 2 for x in data]
    variance = sum(deviations) / n
    return variance

def stdev(data):
    var = variance(data)
    std_dev = math.sqrt(var)
    return std_dev

#making random team scores
#print(NormalDist(10, 2).inv_cdf(random.random()))

#getting some variables setup
teams = list()
scores = list()
schedule_teams = list()
schedule_scores = list()
schedule_included = False
checking = False
three_weeks = False
avg_score = list()
dev_score = list()
num_wins = list()
sim_wins = list()
tot_wins = list()
tie_detector = list()
tie_breaker = list()
placements = list()
probabilities = list()
PLAYOFFS = list()

#enter file name, prolly need to add a 'make text file' bit of code if none
fname = input("Enter file name:")
try:
    fhand = open(fname)
except:
    fname = 'input.txt'
    fhand = open(fname)

#check if schedule is included, and if 3 weeks have passed
for line in fhand:
    line = line.rstrip()
    if re.search('Schedule', line):
        schedule_included = True
    if re.search('Scores', line):
        checking = True
    if checking == True:
        if re.search('Week 3', line):
            three_weeks = True
checking = False
if schedule_included == False:
    print('Please enter the schedule, then rerun the code.')
    exit()
if three_weeks == False:
    print('Three weeks of data are needed. Please wait until more data is acquired.')
    exit()

#get season data: team names, # of teams, # of weeks, current week
fhand = open(fname)
count = 0
counta = 0
for line in fhand:
    line = line.rstrip()
    if re.search('versus', line):
        words = line.split()
        teamname1 = words[0]
        teamname2 = words[2]
        if teamname1 not in teams:
            teams.append(teamname1)
        if teamname2 not in teams:
            teams.append(teamname2)
    if re.search('Scores', line):
        checking = True
    if checking == False:
        if re.search('Week', line):
            count = count + 1
    else:
        if re.search('Week', line):
            counta = counta + 1
num_teams = len(teams)
cur_week = counta
num_totweeks = count
x = 0
#setting up lists of lists
for i in range(num_teams):
    scores.append([])
    tie_detector.append([])
    tie_breaker.append([])
    placements.append([])
    probabilities.append([])
    num_wins.append(x)
    sim_wins.append(x)
    PLAYOFFS.append(x)
for j in range(num_teams):
    placements[j] = [0] * num_teams
    probabilities[j] = [0] * num_teams

#updating team scores. kinda bullshit. surely a better way exists...
#getting averages and standard dev
count = 0
fhand = open(fname)
for line in fhand:
    line = line.rstrip()
    if re.search('versus', line):
        words = line.split()
        schedule_teams.append(words[0])
        schedule_teams.append(words[2])
    if re.search('[0-9] to [0-9]', line):
        words = line.split()
        schedule_scores.append(int(words[0]))
        schedule_scores.append(int(words[2]))
#getting each team's scores
for each in schedule_teams:
    scores[teams.index(each)].append(schedule_scores[count])
    count += 1
    if count >= cur_week * num_teams:
        break
for each in scores:
    avg_score.append(mean(each))
    dev_score.append(stdev(each))
#error handling a standard dev of 0
for i in range(len(teams)):
    if dev_score[i] == 0:
        dev_score[i] = 0.001

#getting wins
for i in range(0, len(schedule_scores) - 1, 2):
    if schedule_scores[i] > schedule_scores[i+1]:
        for team in teams:
            if team == schedule_teams[i]:
                num_wins[teams.index(team)] += 1
    elif schedule_scores[i] < schedule_scores[i+1]:
        for team in teams:
            if team == schedule_teams[i+1]:
                num_wins[teams.index(team)] += 1
    else:
        print('There was a tie in the real scores.')

#so all that shit up there was just to get the current standings..
#now onto simulation
try:
    n = int(input('How many loops for the simulation? '))
except:
    n = 4

#this method is for fantasy football, different method required for goalty
for i in range(n):
    for j in range(len(schedule_scores), len(schedule_teams) - 1, 2):
#comparing simulated scores
#teama/teamb return the index number (in the teams list) of the teams playing
        teama = teams.index(schedule_teams[j])
        teamb = teams.index(schedule_teams[j+1])
        scorea = NormalDist(avg_score[teama], dev_score[teama]).inv_cdf(random.random())
        scoreb = NormalDist(avg_score[teamb], dev_score[teamb]).inv_cdf(random.random())
        if scorea > scoreb:
            sim_wins[teama] += 1
        elif scorea < scoreb:
            sim_wins[teamb] += 1
        else:
            print('There was a tie in the simulation.')
            sim_wins[teama] += .5
            sim_wins[teamb] += .5
    tot_wins = [a+b for a,b in zip(sim_wins, num_wins)]
#detecting ties
    for k in range(len(tot_wins)):
        for m in range(len(tot_wins)):
            if tot_wins[k] == tot_wins[m]:
                tie_detector[k].append(1)
            else:
                tie_detector[k].append(0)
#awarding tie breaker to higher avg score
    for k in range(len(avg_score)):
        for m in range(len(avg_score)):
            if avg_score[k] > avg_score[m]:
                tie_breaker[k].append(1)
            else:
                tie_breaker[k].append(0)
    award = []
    for x,y in zip(tie_detector, tie_breaker):
        temp = []
        for l, m in zip(x,y):
            temp.append(l * m)
        award.append(sum(temp))
#figuring out ranking
    seq = sorted(tot_wins)
    i_rank = [seq.index(v) for v in tot_wins]
    rank = [a+b for a,b in zip(i_rank, award)]
#keeping track of who finishes where
    count = 0
    for each in rank:
        for place in range(num_teams - 1, -1, -1):
            if each == place:
                placements[rank.index(each)][count] += 1
            count += 1
        count = 0
#reset things
    for k in range(len(sim_wins)):
        sim_wins[k] = 0
    for each in tie_detector:
        each.clear()
    for each in tie_breaker:
        each.clear()

#holy moly what a for loop
#now for probabilities
count = 0
for i in range(num_teams):
    for j in range(num_teams):
        probabilities[i][j] = round(placements[i][j] * 100 / n, 1)
for each in probabilities:
    x = 0
    for i in range(4):
        x = x + each[i]
    PLAYOFFS[count] = round(x, 1)
    count += 1

with open('output.txt', 'w') as f:
    for i in range(num_teams):
        f.write(teams[i] + ':' + '\n')
        f.write('   First ' + str(probabilities[i][0]) + '%, ')
        f.write('   Second ' + str(probabilities[i][1]) + '%, ')
        f.write('   Third ' + str(probabilities[i][2]) + '%, ')
        f.write('   Fourth ' + str(probabilities[i][3]) + '%\n\n')
        f.write('   PLAYOFFS??! ' + str(PLAYOFFS[i]) + '%\n\n')
