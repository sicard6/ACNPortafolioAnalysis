import pyomo.environ as pe
import pandas as pd
import os, sys
print(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path[0] =os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
import src.optimization.model.Constraints.constraints as constraints
import src.optimization.model.preprocess_data as data
from src.commons.system_util import SystemUtilities

def set_set(model, to_pyomo_returns):
    model.time_dim = pe.RangeSet(len(to_pyomo_returns.time_set))
    model.assets = pe.Set(initialize=to_pyomo_returns.assets_set)
    return model

def set_parameters(model, to_pyomo_return, to_pyomo_mean):
    model.returns = pe.Param(model.time_dim, model.assets, initialize=to_pyomo_return.dict)
    model.return_mean = pe.Param(model.assets, initialize=to_pyomo_mean.dict)
    print(to_pyomo_mean.dict)
    return model

def set_variables(model):
    model.x = pe.Var(model.assets, domain=pe.NonNegativeReals)
    model.y = pe.Var(model.time_dim, domain=pe.NonNegativeReals)
    return model

def set_objetive_function(model, preprocess_data):
    model.obj = pe.Objective(expr=preprocess_data.coefficient*sum(model.x[i]*model.return_mean[i] for i in model.assets))-(1/len(model.time_dim)*sum(model.y[i] for i in model.time_dim))
    return model

def set_constraints(model):
    model = constraints.constraint_1(model)
    model = constraints.constraint_2(model)
    model = constraints.constraint_3(model)
    return model

def optimize(model):
    solver = pe.SolverFactory('glpk')
    result = solver.solve(model)
    return solver, result

def make_model(to_pyomo_returns, to_pyomo_mean, preprocess_data):
    model = pe.ConcreteModel("version 1")
    model = set_set(model, to_pyomo_returns)
    model = set_parameters(model, to_pyomo_returns, to_pyomo_mean)
    model = set_variables(model)
    model = set_constraints(model)
    model = set_objetive_function(model, preprocess_data)
    solver, result = optimize(model)
    return model, solver, result


system_util = SystemUtilities()
system_util.read_parameters()
system_util.generate_parameters()
parameters = system_util.parameters
x = data.preprocess_data(parameters)
to_pyomo_returns =data.data_to_pyomo(x.returns)
to_pyomo_mean =data.data_to_pyomo(x.returns_mean)

make_model(to_pyomo_returns, to_pyomo_mean, x)











