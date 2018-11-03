# Monty Hall Simulator - Single Thread
#######################################
# Author: Dave Auld
# Version: 1.2
# Date: 10th September 2018
# Description: Monty Hall Simulation
# using single thread.
# 
# License: MIT
#######################################

import argparse                             # argparse added to support command line parameter functionality
from random import randint, choice          # used for selections
from timeit import default_timer as timer   # used for timing the runs.

# Application Defaults
numberOfRounds = 1000                       # Set default for number of rounds
roundOutput = False                         # Set default for display of individual round output

# Setup the argparse
parser = argparse.ArgumentParser(prog="montyhallsim", 
                                    description='''Monty Hall Simulation. This is a basic Monty Hall Simulation, the program will run for a given number of rounds  
                                            and display the number of wins for the different methods (stick/random/swap).''', 
                                    epilog='''For more information on the Monty Hall paradox, visit; \n
                                        https://en.wikipedia.org/wiki/Monty_Hall_problem''')
# Sdd argument for displaying the round output.
parser.add_argument("-o", "--output", action="store_true", help="Display individual round output. Default is hidden.")
parser.add_argument("-r", "--rounds", nargs=1, type=int, default=1000, help="Set the number of rounds. Integer. Default is 1000.")
args = parser.parse_args()

if args.output:
     roundOutput=True

if args.rounds:
    if type(args.rounds) is int:            # If not supplied on cli, defaults value returns int type
        numberOfRounds = args.rounds
    elif type(args.rounds) is list:         # If supplied on cli, it returns a list of int, need 1st one.
        numberOfRounds = args.rounds[0]
        if numberOfRounds == 0:             # Prevent user providing 0 as a number
            numberOfRounds = 1

# current round array contains, [RoundNumber, WinningNumber, ParticipantPick, HostShow, ResultStick, ResultRandom, ResultSwap]
round = [0,0,0,0,False,False,False]

# count of wins for each strategy, stick, random, swap
results = [0,0,0]

# Timings for Run
startTime = timer()
finsihTime = timer()

def main():
    # Initialise current round by setting up the winning number
    print("Monty Hall Simulator, 3 boxes.")
    print("Number of Rounds: " + str(numberOfRounds))
    if roundOutput == True:
        print("RoundNumber, WinningNumber, ParticipantPick, HostShow, ResultStick, ResultRandom, ResultSwap")

    for round[0] in range(numberOfRounds):
        runRound()
    else:
        finsihTime = timer()
        duration = finsihTime - startTime
        print("Results for Number of Rounds: " + str(numberOfRounds))
        print("============================================================")
        print("Duration, " + str(duration) + " seconds.")
        print("Stick  = " + str(results[0]) + " : " + str((float(results[0]) / numberOfRounds) * 100) + " %")
        print("Random = " + str(results[1]) + " : " + str((float(results[1]) / numberOfRounds) * 100) + " %")
        print("Swap   = " + str(results[2]) + " : " + str((float(results[2]) / numberOfRounds) * 100) + " %")

def runRound():
    # Increment Round Number
    round[0] += 1

    # Select the rounds winning box, random choice
    round[1] = randint(1,3)

    # Select the participant random choice
    round[2] = randint(1,3)

    # Host does their reveal next.
    hostPick()

def hostPick():
    #host compares winning box with participant choice and shows a losing box
    
    # 1st Case, Participant has chosen the right box
    if round[1] == round[2]:
        if round[1] == 1:
            round[3] = choice([2,3])    #Participant Pick 1, Host Show 2 or 3
        if round[1] == 2:
            round[3] = choice([1,3])    #Participant Pick 2, Host Show 1 or 3
        if round[1] == 3:
            round[3] = choice([1,2])    #Participant Pick 3, Host Show 1 or 2

    # 2nd Case, Participant has chosen the wrong box
    if round[1] != round[2]:
        if round[1] == 1 and round[2] == 2:
            round[3] = 3    #Participant Picked 1, correct is 2, Host Show 3
        if round[1] == 1 and round[2] == 3:
            round[3] = 2    #Participant Picked 1, correct is 3, Host Show 2
        if round[1] == 2 and round[2] == 1:
            round[3] = 3    #Participant Picked 2, correct is 1, Host Show 3
        if round[1] == 2 and round[2] == 3:
            round[3] = 1    #Participant Picked 2, correct is 3, Host Show 3
        if round[1] == 3 and round[2] == 1:
            round[3] = 2    #Participant Picked 3, correct is 1, Host Show 2
        if round[1] == 3 and round[2] == 2:
            round[3] = 1    #Participant Picked 3, correct is 2, Host Show 1

    #Participant has their 2nd choice next
    participantChoiceResult()

def participantChoiceResult():
    # 1st Case Participant Sticks
    if round[1] == round[2]:
        round[4] = True
        results[0] += 1         # Increment Win count
    else:
        round[4] = False

    # 2nd Case Participant Picks Random box from remaining 2
    if round[3] == 1:
        if choice([2,3]) == round[1]:
            round[5] = True
            results[1] += 1     # Increment Win count
        else:
            round[5] = False
    
    if round[3] == 2:
        if choice([1,3]) == round[2]:
            round[5] = True
            results[1] += 1     # Increment Win count
        else:
            round[5] = False
    
    if round[3] == 3:
        if choice([1,2]) == round[2]:
            round[5] = True
            results[1] += 1     # Increment Win count
        else:
            round[5] = False

    # 3rd Case Participant Swaps box
    if round[2] == round[1]:
        #If Participant had originally picked winning number, then loses.
        round[6] = False
    else:
        round[6] = True
        results[2] += 1         # Increment win count
    
    #Show round output
    if roundOutput == True:
        printRoundOutput()

def printRoundOutput():
    # Display the ouptut for the current round
    print(str(round[0]) + ":" + str(round[1]) + ":" + str(round[2]) + ":" + str(round[3]) + ":" + str(round[4]) + ":" + str(round[5]) + ":" + str(round[6]))

# Let's Go!
main()
