import statsmodels.api as sm 
import statsmodels.formula.api as smf
import statsmodels.graphics.api as smg
from sklearn import model_selection  
from sklearn import linear_model
import patsy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from collections import Counter

def first_word(s):
    s = s.strip()
    for i in range(len(s)):
        if s[i] == ' ':
            return s[:i]
    return s

df_car = pd.read_csv("CAR DETAILS FROM CAR DEKHO.csv")

df_car['first'] = df_car.name.apply(first_word)
df_car['year'] = 2022 - df_car.year

df = df_car[df_car['first'] == 'Maruti']

df_fuel = pd.get_dummies(df.fuel)
df_seller = pd.get_dummies(df.seller_type)
df_transmission = pd.get_dummies(df.transmission)
df_age = df.year 
df_km_driven = df.km_driven

df_data = pd.concat([df_fuel,df_seller,df_transmission,df_age], axis=1, join='inner')

X = df_data

y = np.log(df.selling_price)

print(y)

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y,train_size = 0.7)

model = linear_model.LinearRegression()
model.fit(X_train, y_train)

print(model.score(X_train, y_train))

print(model.score(X_test, y_test))

model = smf.ols('y~df_fuel+df_seller+df_transmission+df_age+df_km_driven', df_data)
result = model.fit()
print(result.summary())
