from ortools.sat.python import cp_model


model = cp_model.CpModel()

base = 10
#1 means that can't be zero and 0 means that can be 0

c = model.NewIntVar(1,base-1,'C')
p = model.NewIntVar(0,base-1,'P')
i = model.NewIntVar(1,base-1,'I')
s = model.NewIntVar(0,base-1,'S')
f = model.NewIntVar(1,base-1,'F')
u = model.NewIntVar(0,base-1,'U')
n = model.NewIntVar(0,base-1,'N')
t = model.NewIntVar(1,base-1,'T')
r = model.NewIntVar(0,base-1,'R')
u = model.NewIntVar(0,base-1,'U')
e = model.NewIntVar(0,base-1,'E')

#We need to group variables in a list to use the constraint AllDifferent
letters = [c,p,i,s,f,u,n,t,r,e]

#Verify that we have enough digits
assert base>=len(letters)


#Defining the constraints
#First, we ensure that all letters have different values,
# using the AddAllDifferent helper method. 
#Then we use the AddEquality helper method 
# to create constraints that enforce the CP + IS + FUN = TRUE equality.

model.AddAllDifferent(letters)
#CP + IS + FUN = TRUE
model.Add(c*base+p + i*base+s + f*base*base+u*base+n == t*base*base*base+r*base*base+u*base+e)


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


