from ortools.sat.python import cp_model


model = cp_model.CpModel()

base = 10
#1 means that can't be zero and 0 means that can be 0
#SEND + MORE = MONEY

s = model.NewIntVar(1,base-1,'S')
e = model.NewIntVar(0,base-1,'E')
n = model.NewIntVar(0,base-1,'N')
d = model.NewIntVar(0,base-1,'D')
m = model.NewIntVar(1,base-1,'M')
o = model.NewIntVar(0,base-1,'O')
r = model.NewIntVar(0,base-1,'R')
y = model.NewIntVar(0,base-1,'Y')


#We need to group variables in a list to use the constraint AllDifferent
letters = [s,e,n,d,m,o,r,y]

#Verify that we have enough digits
assert base>=len(letters)


#Defining the constraints
#First, we ensure that all letters have different values,
# using the AddAllDifferent helper method. 
#Then we use the AddEquality helper method 
# to create constraints that enforce the CP + IS + FUN = TRUE equality.

model.AddAllDifferent(letters)
#CP + IS + FUN = TRUE
model.Add( s*base*base*base + e*base*base+ n*base + d + m*base*base*base + o*base*base + r*base + e == m*base*base*base*base+o*base*base*base+n*base*base+e*base+y)



class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count+=1
        for v in self.__variables:
            print(' %s = %i' % (v, self.Value(v)),end = ' ')
        print()

    def solution_count(self):
        return self.__solution_count

#Invoking the solver
solver = cp_model.CpSolver()
solution_printer = VarArraySolutionPrinter(letters)
#Enumerate all solutions
solver.parameters.enumerate_all_solutions = True
#Solve
status = solver.Solve(model, solution_printer)

print('\nStatistics')
print(f'  status   : {solver.StatusName(status)}')
print(f'  conflicts: {solver.NumConflicts()}')
print(f'  branches : {solver.NumBranches()}')
print(f'  wall time: {solver.WallTime()} s')
print(f'  sol found: {solution_printer.solution_count()}')


