import pyomo.environ as pe
#Cambiar estos nombre-Preguntar a Vale
def constrain_1(model, j, t):
    rule_exp = sum(model.x[j]*(model.returns[t,j]-model.return_mean[j])for j in model.assets <= model.y[t])
    model.constrain_1 = pe.Constraint(model.assets, model.time_dim, rule=rule_exp)
    return model

def constrain_2(model, j, t):
    rule_exp = sum(model.x[j]*(model.returns[t,j]-model.return_mean[j])for j in model.assets <= -1*model.y[t])
    model.constrain_2 = pe.Constraint(model.assets, model.time_dim, rule=rule_exp)
    return model

def constrain_3(model, j):
    rule_exp = sum(model.x[j] for j in model.assets) == 1
    model.constrain_3 = pe.Constraint(model.assets, rule=rule_exp)