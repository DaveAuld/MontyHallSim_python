# MontyHallSim_python
**Monty Hall Simulation in Python**

This is a probability simulation of which a more extended description can be found on Wikipedia at;
https://en.wikipedia.org/wiki/Monty_Hall_problem

In summary, a contestant is given a choice of 3 options, the host knows where the winning option is.
The host then shows the contest one of the losing options.
The contestant can then either stick with their original choice or swap their choice to the other unrevealed option.
In addition to the stick or swap, the simulation also has a third option of where the contestant random picks from the 2 unrevealed options.

The simulation will run for x number of rounds.

The simulation will then output the duration of the run, and also the number of rounds performed.
The output will include the 3 options, stick, swap or random and show the number of times where the contestant would have won for each of these options and the percentage.

From a probability point of view, the results demonstrate that the contestant should always swap as this has the highest chance of winning at 66%.

The results are typically always around the following;
stick = 33%
random = 50%
swap = 66%

**Command Line Options**  
The command line can take parameters as follows;  
`-o, --output`    This flag will turn on individual round output on the display, hidden by default.  
`-r, --round ROUNDS`  This parameter will set the number of rounds to ROUNDS. Default is 1000.  

For the default, with no command line options set, the output will look as follows;  

```Monty Hall Simulator, 3 boxes.
Number of Rounds: 1000
Results for Number of Rounds: 1000
============================================================
Duration, 0.00724301279015 seconds.
Stick  = 329 : 32.9 %
Random = 492 : 49.2 %
Swap   = 671 : 67.1 %
```

If you do select the `--output` option then you will see the addition of the following;
```
RoundNumber, WinningNumber, ParticipantPick, HostShow, ResultStick, ResultRandom, ResultSwap
1:3:1:2:False:False:True
2:2:1:3:False:False:True
3:3:2:1:False:True:True
4:1:3:2:False:False:True
5:3:3:1:True:True:False
etc......
```
