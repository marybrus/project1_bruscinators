import matplotlib.pyplot as plt
import time
import random
import numpy as np

Num_Vars=3
Num_Clauses=4
wff=[[1,-2,-2],[2,3,3],[-1,-3,-3],[-1,-2,3],[1,2,-3]]


# Following is an example of a wff with 3 variables, 3 literals/clause, and 8 clauses
Num_Clauses=8
wff=[[-1,-2,-3],[-1,-2,3],[-1,2,-3],[-1,2,3],[1,-2,-3],[1,-2,3],[1,2,-3],[1,2,3]]

def parse_file(file_path):
    test_cases = []  # This will store the list of lists

    # Oopen file to read
    with open(file_path, 'r') as file:
        for line in file:
            # strip whitespaces and split the line into elements
            numbers = list(map(int, line.strip().split()))
            test_cases.append(numbers)

    # return formatted lists
    return test_cases

def plot_results(sizes, times, flags):
    # This function generates a time/ literal versus number of variables graph

    #initialize the figure size
    plt.figure(figsize=(10, 6))

    # create set so we do not repeat labels
    added_labels = set()

    # lists to store unsatifiable times and sizes
    unsat_sizes = []
    unsat_times = []

    # loop through results
    for i in range(len(sizes)):
        # if satisfiable
        if flags[i]:
            label = 'Satisfiable'
            # plot with as a green circle with the label 'Satisfiable'
            if label not in added_labels:
                plt.scatter(sizes[i], times[i], color='green', marker='o', label=label)
                added_labels.add(label)
            else:
                plt.scatter(sizes[i], times[i], color='green', marker='o')  # No label
        else:
            # if not satisfiable
            label = 'Unsatisfiable'
            if label not in added_labels:
                plt.scatter(sizes[i], times[i], color='red', marker='^', label=label)
                added_labels.add(label)
            else:
                plt.scatter(sizes[i], times[i], color='red', marker='^')  # No label

            #store specific unsat 
            unsat_sizes.append(sizes[i])
            unsat_times.append(times[i])

    # label axis and title
    plt.xlabel('Number of Variables')
    plt.ylabel('Execution Time (μs) / Literals')
    plt.title('Time vs. Variables with Line of Best Fit for Unsatisfied')

  
    if unsat_sizes:
        #Basically making a line of beset fit for the plot
        log_unsat_times = np.log(unsat_times)

        fit = np.polyfit(unsat_sizes, log_unsat_times, 1)  # Linear fit to log(time) vs. size
        a = np.exp(fit[1])  # a = exp(intercept)
        b = fit[0]          # b is the slope

        def exp_fit(x):
            return a * np.exp(b * x)

        # generate axis for exp line
        sizes_fit = np.linspace(min(unsat_sizes), max(unsat_sizes), 100)
        times_fit = exp_fit(sizes_fit)

        # plot exp line
        plt.plot(sizes_fit, times_fit, '--k', label=f'Best Fit (Unsatisfied): y = {a:.2f} * e^({b:.2f}x)')

    plt.legend()
    plt.grid(True)

    # save and show plot
    plt.savefig("plot_bruscinator.png")
    plt.show()
    plt.close()



def increment(assignment):
    # Go through each element for assignment
    for i in range(len(assignment)):
        if assignment[i] == 0:
            # if zero, change to 1 and return true
            assignment[i] = 1
            return True
        # If it is 1, reset to zero
        assignment[i] = 0

    # Else return false
    return False


def check(Wff, Nvars, Nclauses, Assignment):
  while True:
    # goes through clauses --> stops if not satisfiable
    Satisfiable = True

    # Loops throguh clauses
    for i in range(Nclauses):
      Clause = Wff[i]
      Clause_Satisfiable = False

      # Loops throguh literals in clause
      for Literal in Clause:
        Var = abs(Literal)
        # Check if literal is satisfied
        if (Literal > 0 and Assignment[Var] == True) or (Literal < 0 and Assignment[Var] == False):
          Clause_Satisfiable = True
          break
      # If not, then is not satisfiable
      if not Clause_Satisfiable:
        Satisfiable = False
        break

    # Returns true if satisfied
    if Satisfiable:
      return True

    # Once no more assignments can be made it returns false
    if not increment(Assignment):
        return False

def build_wff(Nvars, Nclauses, LitsPerClause):
  # this wills tore well formed formulas
  wff=[]

  # Loop through clauses
  for i in range(1,Nclauses+1):
    clause=[]

    # Loop through literals per clause
    for j in range(1,LitsPerClause+1):

      # Randomly decide which are negated
      var=random.randint(1,Nvars)
      if random.randint(0,1)==0: var=-var
      # Add the variable to the clause
      clause.append(var)
    # Add the clause to the well formed formulas
    wff.append(clause)
  return wff

def test_wff(wff,Nvars,Nclauses):
  # Initialize assignment
  Assignment=list((0 for x in range(Nvars+2)))

  # Start timer
  start = time.time() # Start timer
  SatFlag=check(wff,Nvars,Nclauses,Assignment)

  # End tier
  end = time.time() # End timer

  # Get elapsed time in microseconds
  exec_time=int((end-start)*1e6)

  # Return the formula, assignment, flag, and time
  return [wff,Assignment,SatFlag,exec_time]

def run_cases(TestCases,ProbNum,resultsfile,tracefile,cnffile):
    # TestCases: list of 4tuples describing problem
    #   0: Nvars = number of variables
    #   1: NClauses = number of clauses
    #   2: LitsPerClause = Literals per clause
    #   3: Ntrials = number of trials
    # ProbNum: Starting nunber to be given to 1st output run
    # resultsfile: path to file to hold output
    # tracefile: path to file to hold output
    # cnffile: path to file to hold output
    # For each randomly built wff, print out the following list
    #   Problem Number
    #   Number of variables
    #   Number of clauses
    #   Literals per clause
    #   Result: S or U for satisfiable or unsatisfiable
    #   A "1"
    #   Execution time
    #   If satisfiable, a binary string of assignments
    if not(ShowAnswer):
        print("S/U will NOT be shown on cnf file")
# Each case = Nvars,NClauses,LitsPerClause,Ntrials
    f1=open(resultsfile+".csv",'w')
    f2=open(tracefile+".csv",'w')
    f3=open(cnffile+".cnf","w")

    # Initialize values to keep track of for print
    sizes = []
    times = []
    satisfiable_flags = []

    #initialize counters for final line of output
    Nwffs=0
    Nsat=0
    Nunsat=0
#    f1.write('ProbNum,Nvars,NClauses,LitsPerClause,Result,ExecTime(us)\n')
    for i in range(0,len(TestCases)):

        TestCase=TestCases[i]
        Nvars=TestCase[0]
        NClauses=TestCase[1]
        LitsPerClause=TestCase[2]
        Ntrials=TestCase[3]
        #Now run the number of trials for this wff configuration
        Scount=Ucount=0
        AveStime=AveUtime=0
        MaxStime=MaxUtime=0
        for j in range(0,Ntrials):
            #generate next trial case for this configuration
            Nwffs=Nwffs+1
            random.seed(ProbNum)
            wff = build_wff(Nvars,NClauses,LitsPerClause)
            results=test_wff(wff,Nvars,NClauses)
            wff=results[0]
            Assignment=results[1]
            Exec_Time=results[3]

            # Add values to lists to be able to plot
            sizes.append(Nvars)
            times.append(Exec_Time/LitsPerClause)
            satisfiable_flags.append(results[2])

            if results[2]:
                y='S'
                Scount=Scount+1
                AveStime=AveStime+Exec_Time
                MaxStime=max(MaxStime,Exec_Time)
                Nsat=Nsat+1
            else:
                y='U'
                Ucount=Ucount+1
                AveUtime=AveUtime+Exec_Time
                MaxUtime=max(MaxUtime,Exec_Time)
                Nunsat=Nunsat+1
            x=str(ProbNum)+','+str(Nvars)+','+str(NClauses)+','+str(LitsPerClause)
            x=x+str(NClauses*LitsPerClause)+','+y+',1,'+str(Exec_Time)
            if results[2]:
                for k in range(1,Nvars+1):
                    x=x+','+str(Assignment[k])
            print(x)
            f1.write(x+'\n')
            f2.write(x+'\n')
            #Add wff to cnf file
            if not(ShowAnswer):
                y='?'
            x="c "+str(ProbNum)+" "+str(LitsPerClause)+" "+y+"\n"
            f3.write(x)
            x="p cnf "+str(Nvars)+" "+str(NClauses)+"\n"
            f3.write(x)
            for i in range(0,len(wff)):
                clause=wff[i]
                x=""
                for j in range(0,len(clause)):
                    x=x+str(clause[j])+","
                x=x+"0\n"
                f3.write(x)
            #Increment problem number for next iteration
            ProbNum=ProbNum+1

        # Store and print results
        counts='# Satisfied = '+str(Scount)+'. # Unsatisfied = '+str(Ucount)
        maxs='Max Sat Time = '+str(MaxStime)+'. Max Unsat Time = '+str(MaxUtime)
        aves='Ave Sat Time = '+str(AveStime/Ntrials)+'. Ave UnSat Time = '+str(AveUtime/Ntrials)
        print(counts)
        print(maxs)
        print(aves)

        # Write to files
        f2.write(counts+'\n')
        f2.write(maxs+'\n')
        f2.write(aves+'\n')
    x=cnffile+",TheBoss,"+str(Nwffs)+","+str(Nsat)+","+str(Nunsat)+","+str(Nwffs)+","+str(Nwffs)+"\n"

    # Close all of the files
    f1.write(x)
    f1.close()
    f2.close()
    f3.close()

    # Plot all of the results
    plot_results(sizes, times, satisfiable_flags)



# Test cases used
"""TestCases = [
    [4, 9, 2, 10],
    [8,18,2,10],
    [12,20,2,10],
    [16,30,2,10],
    [18,32,2,10],
    [20,33,2,10],
    [22,38,2,10]
]"""
file_path = 'input_bruscinator.txt'  # Replace with the actual file path
TestCases = parse_file(file_path)

# We want to  show the solution
ShowAnswer = True
ProbNum = 3

# Where to store the files
resultsfile = 'output_resultsfile_bruscinator'
tracefile = 'output_tracefile_bruscinator'
cnffile = 'output_cnffile_bruscinator'

# Run all test cases
run_cases(TestCases, ProbNum, resultsfile, tracefile, cnffile)
