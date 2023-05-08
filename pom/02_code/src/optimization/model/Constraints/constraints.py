import pyomo.environ as pe
#Cambiar estos nombre-Preguntar a Vale
def constraint_1_rule(model, j, t):
    rule_exp = sum(model.x[j]*(model.returns[t,j]-model.return_mean[j]) for j in model.assets)
    return rule_exp <= model.y[t]

def constraint_1(model):
    model.constrain_1 = pe.Constraint(model.assets, model.time_dim, rule=constraint_1_rule)
    return model

def constraint_2_rule(model, j, t):
    rule_exp = sum(model.x[j]*(model.returns[t,j]-model.return_mean[j])for j in model.assets) 
    return rule_exp <= -1*model.y[t]

def constraint_2(model):
    model.constrain_2 = pe.Constraint(model.assets, model.time_dim, rule=constraint_2_rule)
    return model

def constraint_3_rule(model, j):
    rule_exp = sum(model.x[j] for j in model.assets) 
    return rule_exp == 1

def constraint_3(model):
    model.constrain_3 = pe.Constraint(model.assets, rule=constraint_3_rule)
    return model