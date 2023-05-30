import pyomo.environ as pe
import os, sys
sys.path[0] =os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
import src.optimization.model.Constraints.constraints as constraints
import src.optimization.model.preprocess_data as data
from src.commons.system_util import SystemUtilities

def set_set(model, to_pyomo_returns):
    """
        Sets the time and assets dimensions of the Pyomo model.

    Parameters:
        model (pyomo.environ.ConcreteModel): The Pyomo model object.
        to_pyomo_returns (PyomoData): The processed data object.

    Returns:
        pyomo.environ.ConcreteModel: The Pyomo model object with the time and assets dimensions set.

    """
    model.time_dim = pe.RangeSet(len(to_pyomo_returns.time_set))
    model.assets = pe.Set(initialize=to_pyomo_returns.assets_set)
    return model

def set_parameters(model, to_pyomo_return, to_pyomo_mean):
    """
        Sets the parameters of the Pyomo model.

    Parameters:
        model (pyomo.environ.ConcreteModel): The Pyomo model object.
        to_pyomo_return (PyomoData): The processed data object containing the returns data.
        to_pyomo_mean (PyomoData): The processed data object containing the expected returns data.

    Returns:
        pyomo.environ.ConcreteModel: The Pyomo model object with the parameters set.

    """
    model.returns = pe.Param(model.time_dim, model.assets, initialize=to_pyomo_return.dict)
    model.return_mean = pe.Param(model.assets, initialize=to_pyomo_mean.dict)
    return model

def set_variables(model):
    """
        Sets the variables of the Pyomo model.

    Parameters:
        model (pyomo.environ.ConcreteModel): The Pyomo model object.

    Returns:
        pyomo.environ.ConcreteModel: The Pyomo model object with the variables set.

    """
    model.x = pe.Var(model.assets, domain=pe.NonNegativeReals)
    model.y = pe.Var(model.time_dim, domain=pe.NonNegativeReals)
    return model

def set_objetive_function(model, preprocess_data):
    """
        Sets the objective function of the Pyomo model.

    Parameters:
        model (pyomo.environ.ConcreteModel): The Pyomo model object.
        preprocess_data (object): The preprocessed data object containing the processed data.

    Returns:
        pyomo.environ.ConcreteModel: The Pyomo model object with the objective function set.

    """
    model.obj = pe.Objective(expr=preprocess_data.coef*sum((model.x[i]*model.return_mean[i]) for i in model.assets)-(1/len(model.time_dim)*sum(model.y[t] for t in model.time_dim)), sense=pe.maximize)
    return model

def set_constraints(model):
    """
        Sets the constraints of the Pyomo model.

    Parameters:
        model (pyomo.environ.ConcreteModel): The Pyomo model object.

    Returns:
        pyomo.environ.ConcreteModel: The Pyomo model object with the constraints set.

    """
    model = constraints.constraint_1(model)
    model = constraints.constraint_2(model)
    model = constraints.constraint_3(model)
    return model

def optimize(model):
    """
        This function solves an optimization problem defined in a Pyomo model object using the GLPK solver and returns the solver
        and the result of the optimization.

    Parameters:
        model (pyomo.environ.ConcreteModel): A Pyomo model object containing the optimization problem to be solved.

    Returns:
        solver (pyomo.opt.base.solvers.SolverFactory): A Pyomo solver object that was used to solve the optimization problem.
        result (pyomo.opt.results.SolverResults): A Pyomo solver result object that contains the results of the optimization.
    """
    solver = pe.SolverFactory('glpk')
    result = solver.solve(model, tee=True)
    return solver, result

def make_model(to_pyomo_returns, to_pyomo_mean, preprocess_data):
    """
        This function creates a Pyomo optimization model, sets the necessary parameters, variables, constraints, and objective
        function to solve a mean-variance portfolio optimization problem, and returns the model, solver, and result of the
        optimization.

    Parameters:
        to_pyomo_returns (list): A list of returns for each asset in the portfolio.
        to_pyomo_mean (float): The target mean return of the portfolio.
        preprocess_data (function): A function that preprocesses the input data.

    Returns:
        model (pyomo.environ.ConcreteModel): A Pyomo model object that contains the optimization problem.
        solver (pyomo.opt.base.solvers.SolverFactory): A Pyomo solver object that was used to solve the optimization problem.
        result (pyomo.opt.results.SolverResults): A Pyomo solver result object that contains the results of the optimization.
    """
    model = pe.ConcreteModel("version 1")
    model = set_set(model, to_pyomo_returns)
    model = set_parameters(model, to_pyomo_returns, to_pyomo_mean)
    model = set_variables(model)
    model = set_constraints(model)
    model = set_objetive_function(model, preprocess_data)
    model.pprint()
    solver, result = optimize(model)
    return model, solver, result
    


system_util = SystemUtilities()
system_util.read_parameters()
system_util.generate_parameters()
parameters = system_util.parameters
x = data.preprocess_data(parameters)
diario = x.returns
mensual = data.data_periodicity(diario, parameters)
mean = x.returns_mean
returns = data.get_next_period(mensual, mean)
to_pyomo_returns =data.data_to_pyomo(returns)
to_pyomo_mean =data.data_to_pyomo(mean)
model, solver, result = make_model(to_pyomo_returns, to_pyomo_mean, x)












