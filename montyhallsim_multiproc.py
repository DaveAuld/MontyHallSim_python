# Monty Hall Simulator - Multi-Process
#######################################
# Author: Dave Auld
# Version: 1.0
# Date: 13th September 2018
# Description: Monty Hall Simulation
# using process pool and queue for 
# sharing any print output to main 
# for handling.
#
# License: MIT
#######################################

import multiprocessing                      # Required to get CPU max logical cores, and support multiprocess/pools
import argparse                             # argparse added to support command line parameter functionality
from random import randint, choice          # used for selections
from timeit import default_timer as timer   # used for timing the runs.
from functools import partial               # used to pass multiple parameters into pool.map

def processRound(currentRound, output):
    # Local Round Data
    round = [0,0,0,0,False,False,False] # [RoundNumber, WinningNumber, ParticipantPick, HostShow, ResultStick, ResultRandom, ResultSwap]
    result = [0,0,0]                    # [stick, random, swap]
    
    # store the round number
    round[0] = currentRound

    # Select the rounds winning box, random choice
    round[1] = randint(1,3)

    # Select the participant random choice
    round[2] = randint(1,3)

    # Host does their reveal next. pass on the local data
    hostPick(round, output, result)

    # Pass result back to caller
    return result

def hostPick(round, output, result):
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
    if round[1] <> round[2]:
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

    # Participant has their 2nd choice next
    participantChoiceResult(round, output, result)

    # Pass result back to caller
    return result

def participantChoiceResult(round, output, result):
    # 1st Case Participant Sticks
    if round[1] == round[2]:
        round[4] = True
        result[0] += 1         # Increment Win count
    else:
        round[4] = False

    # 2nd Case Participant Picks Random box from remaining 2
    if round[3] == 1:
        if choice([2,3]) == round[1]:
            round[5] = True
            result[1] += 1     # Increment Win count
        else:
            round[5] = False
    
    if round[3] == 2:
        if choice([1,3]) == round[2]:
            round[5] = True
            result[1] += 1     # Increment Win count
        else:
            round[5] = False
    
    if round[3] == 3:
        if choice([1,2]) == round[2]:
            round[5] = True
            result[1] += 1     # Increment Win count
        else:
            round[5] = False

    # 3rd Case Participant Swaps box
    if round[2] == round[1]:
        # If Participant had originally picked winning number, then loses.
        round[6] = False
    else:
        round[6] = True
        result[2] += 1         # Increment Win count
    
    #Show round output
    if output:
        printRoundOutput(round)

    # Pass result back to caller
    return result

def printRoundOutput(round):
    # Place the output text for the current round onto the shared queue.
    text = str(round[0]) + ":" + str(round[1]) + ":" + str(round[2]) + ":" + str(round[3]) + ":" + str(round[4]) + ":" + str(round[5]) + ":" + str(round[6]) + ":" + multiprocessing.current_process().name
    outputQ.put(text)
    
def initProc(outQ):
    # Used by the process pool to initialize the shared global queue on the child processes
    global outputQ          # The shared queue
    outputQ = outQ

if __name__ == "__main__":

    # Defaults
    processLimit = multiprocessing.cpu_count()  # Process Limit
    numberOfRounds = 1000                       #
    roundOutput = False     

    # Setup the argparse
    parser = argparse.ArgumentParser(prog="montyhallsim", 
                                    description='''Monty Hall Simulation. This is a basic Monty Hall Simulation, the program will run for a given number of rounds  
                                            and display the number of wins for the different methods (stick/random/swap).''', 
                                    epilog='''For more information on the Monty Hall paradox, visit; \n
                                        https://en.wikipedia.org/wiki/Monty_Hall_problem''')
    # Add argument for displaying the round output.
    parser.add_argument("-o", "--output", action="store_true", help="Display individual round output. Default is hidden.")
    parser.add_argument("-r", "--rounds", nargs=1, type=int, default=numberOfRounds, help="Set the number of rounds. Integer. Default is " + str(numberOfRounds) +".")
    parser.add_argument("-t", "--procs", nargs=1, type=int, default=processLimit, help="Set the number of processes. Integer. Default is CPU Logical Cores. " + str(processLimit))
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

    if args.procs:
        if type(args.procs) is int:             # If not supplied on cli, defaults value returns int type
            processLimit = args.procs
        elif type(args.procs) is list:          # If supplied on cli, it returns a list of int, need 1st one.
            processLimit = args.procs[0]
            if processLimit == 0:               # Prevent user providing 0 as a number
                processLimit = 1

    # count of wins for each strategy, stick, random, swap, 
    finalResults = [0,0,0]

    print("Monty Hall Simulator, 3 boxes.")
    print("Number of Rounds: " + str(numberOfRounds))
    print("Number of processes: " + str(processLimit))
    print("============================================================")
    if roundOutput == True:
        print("RoundNumber, WinningNumber, ParticipantPick, HostShow, ResultStick, ResultRandom, ResultSwap")
        print("============================================================")

    # Global queue for passing print output from pool processes to main for display
    outputQ = multiprocessing.Queue()

    # Variable for passing multiple arguments to the process.map
    target =  partial(processRound, output=roundOutput)

    # Timestamp for start
    startTime = timer()
    
    # Setup the pool and initiate the work
    p = multiprocessing.Pool(processLimit, initializer=initProc, initargs=(outputQ, ))
    results = p.map(target, range(numberOfRounds))
    
    # Check if we have child processes in the pool and the shared queue is not empty
    # print the queue to the standard output.
    while not (outputQ.empty() and (p._pool.count > 0)):
        print(outputQ.get_nowait())
    p.close()
    p.join()

    # Aggregate results from pool results.
    for result in results:
        finalResults[0] += result[0]
        finalResults[1] += result[1]
        finalResults[2] += result[2]

    # Timestamo for finish
    finsihTime = timer()
    duration = finsihTime - startTime   # Calculate the duration (seconds).

    print("Results for " + str(numberOfRounds) + " rounds, using " + str(processLimit) + " processes.")
    print("============================================================")
    print("Duration, " + str(duration) + " seconds.")
    print("Stick  = " + str(finalResults[0]) + " : " + str((float(finalResults[0]) / numberOfRounds) * 100) + " %")
    print("Random = " + str(finalResults[1]) + " : " + str((float(finalResults[1]) / numberOfRounds) * 100) + " %")
    print("Swap   = " + str(finalResults[2]) + " : " + str((float(finalResults[2]) / numberOfRounds) * 100) + " %")
    