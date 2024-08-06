from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union
from pulp import LpMaximize, LpMinimize, LpProblem, LpVariable, lpSum, LpStatus,GLPK
import subprocess
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Variable(BaseModel):
    name: str
    low_bound: float = 0
    up_bound: Union[float, None] = None
    cat:str

class Constraint(BaseModel):
    expression: List[float]
    variables: List[str]
    constant: float
    sense: str

class OptimizationProblem(BaseModel):
    objective_coeffs: List[float]
    objective_vars: List[str]
    constraints: List[Constraint]
    sense: str
    variables: List[Variable]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/solve")
def solve_problem(problem: OptimizationProblem):
    if problem.sense == "maximize":
        lp_problem = LpProblem("Optimization-Problem", LpMaximize)
    elif problem.sense == "minimize":
        lp_problem = LpProblem("Optimization-Problem", LpMinimize)
    else:
        raise HTTPException(status_code=400, detail="Invalid sense")

    # Create variables
    variables = {}
    for var in problem.variables:
        variables[var.name] = LpVariable(var.name, lowBound=var.low_bound, upBound=var.up_bound,cat=var.cat)

    # Set objective function
    objective = lpSum([problem.objective_coeffs[i] * variables[problem.objective_vars[i]] for i in range(len(problem.objective_coeffs))])
    lp_problem += objective

    # Add constraints
    for constraint in problem.constraints:
        expression = lpSum([constraint.expression[i] * variables[constraint.variables[i]] for i in range(len(constraint.expression))])
        if constraint.sense == "<=":
            lp_problem += (expression <= constraint.constant)
        elif constraint.sense == ">=":
            lp_problem += (expression >= constraint.constant)
        elif constraint.sense == "==":
            lp_problem += (expression == constraint.constant)
        else:
            raise HTTPException(status_code=400, detail="Invalid constraint sense")

    try:
        print("Tonga eto")
        output_file = "glpk_solution.txt"
        # Solve the problem
        status = lp_problem.solve(solver=GLPK(msg=True, options=["--write", output_file]))
        print("Vita")
        analyse=''
        with open(output_file, "r") as file:
            lines = file.readlines()
            for line in lines:
                analyse += line.strip()+"\n"

        result = {
        "status": LpStatus[lp_problem.status],
        "variables": {v.name: v.varValue for v in lp_problem.variables()},
        "objective": lp_problem.objective.value(),
        "analysis": analyse
    }

        return result
    except Exception as e:
        print(e)
