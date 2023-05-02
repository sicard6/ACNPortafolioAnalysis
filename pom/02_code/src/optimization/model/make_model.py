import pyomo.environ as pe
import pandas as pd
import os, sys
sys.path[0] =os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
import src.optimization.model.Constraints.constraints as constraints

def set_set(model, to_pyomo_returns):
    model.time_dim = pe.RangeSet(to_pyomo_returns.time_set)
    model.assets = pe.Set(initialize=to_pyomo_returns.assets_set)
    return model

def set_parameters(model, to_pyomo_return, to_pyomo_mean):
    model.returns = pe.Param(model.time_dim, model.assets, initialize=to_pyomo_return.dict)
    model.return_mean = pe.Param(model.assets, initialize=to_pyomo_mean.dict)
    return model

def set_variables(model):
    model.x = pe.Var(model.assets, domain=pe.NonNegativeReals)
    model.y = pe.Var(model.tim_dim, domain=pe.NonNegativeReals)

def set_objetive_function(model, preprocess_data):
    model.obj = pe.Objective(expr=preprocess_data.coefficient*sum(model.x[i]*model.return_mean[i] for i in model.assets))-(1/len(model.time_dim)*sum(model.y[i] for i in model.time_dim))









