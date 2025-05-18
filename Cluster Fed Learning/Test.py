import pickle

with open('global_model.pkl','rb') as f:
    params = pickle.load(f)
params['coef'] = params['coef'] * 10**8
params['intercept'] = params['intercept'] * 10**8
print(params['coef'])
print(params['intercept'])
params['coef'] = params['coef'] * 10**-8
params['intercept'] = params['intercept'] * 10**-8
print(params['coef'])
print(params['intercept'])