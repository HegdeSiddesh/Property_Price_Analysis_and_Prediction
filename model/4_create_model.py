import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from xgboost import XGBRegressor
import category_encoders as ce
import json
import pickle

data = pd.read_csv("../data/gurgaon_properties_post_feature_selection_top_12.csv")

with open('model_config.json', 'r') as config_file:
    config = json.load(config_file)

print(config)

X = data.drop(columns=['price'])
y = np.log1p(data['price'])

numerical_cols = ['bedRoom', 'bathroom', 'built_up_area', 'study room', 'servant room', 'store room', 'pooja room']
categorical_cols = ['property_type', 'sector', 'balcony', 'agePossession', 'furnishing_type']

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numerical_cols),
    ('cat', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1), categorical_cols),
    ('cat2', OneHotEncoder(drop='first', handle_unknown='ignore'), ['property_type', 'agePossession']),
    ('cat3', ce.TargetEncoder(), ['sector'])
], remainder='passthrough')

model = RandomForestRegressor
if config['model_name']=='XGBRegressor':
    model = XGBRegressor
if config['model_name']=='ExtraTreesRegressor':
    model = ExtraTreesRegressor

#del config['model_name']
    
params = config['model_parameters']

model_in = model(**params)
additional_params = {'n_jobs' : -1}
model_in.set_params(**additional_params)


pipeline = Pipeline([
    ('preprocess', preprocessor),
    ('regressor', model_in)
])

pipeline.fit(X,y)

with open("final_model.pkl", "wb") as model_file:
    pickle.dump(pipeline, model_file)

with open("final_data.pkl", "wb") as data_file:
    pickle.dump(X, data_file)
