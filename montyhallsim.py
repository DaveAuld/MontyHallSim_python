#Monty Hall Simulator
from random import randint, choice
from timeit import default_timer as timer


#Setup default number of rounds
numberOfRounds = 1000

#Display individual round output
roundOutput = True

#current round array contains, [RoundNumber, WinningNumber, ParticipantPick, HostShow, ResultStick, ResultRandom, ResultSwap]
round = [0,0,0,0,False,False,False]

#count of wins for each strategy, stick, random, swap
results = [0,0,0]

#Timings for Run
startTime = timer()
finsihTime = timer()

def main():
    #initialise current round by setting up the winning number
    print("Monty Hall Simulator, 3 boxes.")
    print("Number of Rounds: " + str(numberOfRounds))
    if roundOutput == True:
        print("RoundNumber, WinningNumber, ParticipantPick, HostShow, ResultStick, ResultRandom, ResultSwap")

    for round[0] in range(numberOfRounds):
        initialPick()
    else:
        finsihTime = timer()
        duration = finsihTime - startTime
        print("Results for Number of Rounds: " + str(numberOfRounds))
        print("============================================================")
        print("Duration, " + str(duration) + " seconds.")
        print("Stick  = " + str(results[0]) + " : " + str((float(results[0]) / numberOfRounds) * 100) + " %")
        print("Random = " + str(results[1]) + " : " + str((float(results[1]) / numberOfRounds) * 100) + " %")
        print("Swap   = " + str(results[2]) + " : " + str((float(results[2]) / numberOfRounds) * 100) + " %")

def initialPick():
    #Increment Round Number
    currentRound = round[0]
    currentRound +=1
    round[0] = currentRound

    # Select the rounds winning box, random choice
    round[1] = randint(1,3)

    # Select the participant random choice
    round[2] = randint(1,3)

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

    participantChoiceResult()

def participantChoiceResult():
    # 1st Case Participant Sticks
    if round[1] == round[2]:
        round[4] = True
    else:
        round[4] = False

    if round[4] == True:
        # Update Score table
        wins = results[0]
        wins += 1
        results[0] = wins

    # 2nd Case Participant Picks Random box from remaining 2
    if round[3] == 1:
        if choice([2,3]) == round[1]:
            round[5] = True
        else:
            round[5] = False
    
    if round[3] == 2:
        if choice([1,3]) == round[2]:
            round[5] = True
        else:
            round[5] = False
    
    if round[3] == 3:
        if choice([1,2]) == round[2]:
            round[5] = True
        else:
            round[5] = False

    if round[5] == True:
        # Update Score Table
        wins = results[1]
        wins += 1
        results[1] = wins

    # 3rd Case Participant Swaps box
    if round[2] == round[1]:
        #If Participant had originally picked winning number, then loses.
        round[6] = False
    else:
        round[6] = True
    
    if round[6] == True:
        # Update Score Table
        wins = results[2]
        wins += 1
        results[2] = wins
    
    #Show round output
    if roundOutput == True:
        printRoundOutput()

def printRoundOutput():
    print(str(round[0]) + ":" + str(round[1]) + ":" + str(round[2]) + ":" + str(round[3]) + ":" + str(round[4]) + ":" + str(round[5]) + ":" + str(round[6]))

#Let's Go!
main()