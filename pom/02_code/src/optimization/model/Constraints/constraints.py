import pyomo.environ as pe
#Cambiar estos nombre-Preguntar a Vale
def constraint_1_rule(model, t):
    """
        This function defines the constraint expression for the first constraint  portfolio optimization model.

    Parameters:
        model (pyomo.environ.ConcreteModel): A Pyomo model object that contains the optimization problem.
        t (int): The time period index for the constraint.

    Returns:
        rule_exp (pyomo.core.expr.numeric_expr.SumExpression): A Pyomo expression object that represents the constraint expression.
    """
    rule_exp = sum(model.x[j]*(model.returns[t,j]-model.return_mean[j]) for j in model.assets)
    return rule_exp <= model.y[t]

def constraint_1(model):
    """
        This function adds the first constraint to the portfolio optimization model.

    Parameters:
        model (pyomo.environ.ConcreteModel): A Pyomo model object that contains the optimization problem.

    Returns:
        model (pyomo.environ.ConcreteModel): The Pyomo model object with the first constraint added.
    """
    model.constrain_1 = pe.Constraint(model.time_dim, rule=constraint_1_rule)
    return model

def constraint_2_rule(model, t):
    """
        This function defines the constraint expression for the second constraint  portfolio optimization model.

    Parameters:
        model (pyomo.environ.ConcreteModel): A Pyomo model object that contains the optimization problem.
        t (int): The time period index for the constraint.

    Returns:
        rule_exp (pyomo.core.expr.numeric_expr.SumExpression): A Pyomo expression object that represents the constraint expression.
    """
    rule_exp = sum(model.x[j]*(model.returns[t,j]-model.return_mean[j]) for j in model.assets) 
    return rule_exp <= -1*model.y[t]

def constraint_2(model):
    """
        This function adds the second constraint to the portfolio optimization model.

    Parameters:
        model (pyomo.environ.ConcreteModel): A Pyomo model object that contains the optimization problem.

    Returns:
        model (pyomo.environ.ConcreteModel): The Pyomo model object with the first constraint added.
    """
    model.constrain_2 = pe.Constraint(model.time_dim, rule=constraint_2_rule)
    return model

def constraint_3_rule(model):
    """
        This function defines the constraint expression for the third constraint  portfolio optimization model.

    Parameters:
        model (pyomo.environ.ConcreteModel): A Pyomo model object that contains the optimization problem.
        t (int): The time period index for the constraint.

    Returns:
        rule_exp (pyomo.core.expr.numeric_expr.SumExpression): A Pyomo expression object that represents the constraint expression.
    """
    rule_exp = sum(1*model.x[j] for j in model.assets) 
    return rule_exp == 1

def constraint_3(model):
    """
        This function adds the third constraint to the portfolio optimization model.

    Parameters:
        model (pyomo.environ.ConcreteModel): A Pyomo model object that contains the optimization problem.

    Returns:
        model (pyomo.environ.ConcreteModel): The Pyomo model object with the first constraint added.
    """
    model.constrain_3 = pe.Constraint(rule=constraint_3_rule)
    return model