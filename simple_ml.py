from keras.models import Sequential
from keras.layers import Dense

import pandas as pd
import numpy as np

from datetime import datetime


df = pd.read_csv('data/exponential.csv')
X = df['key'].values.reshape(-1,1)
y = df['value'].values.reshape(-1,1)

model = Sequential()
model.add(Dense(32, activation='relu', input_shape=(1,)))
model.add(Dense(32,activation='sigmoid'))
model.add(Dense(1))

model.compile(optimizer='adam',loss='mean_absolute_error')

start_build = datetime.now()
model.fit(X,y,epochs=64,batch_size=128)
print('Build Time: ',datetime.now() - start_build)

start_predict = datetime.now()
preds = model.predict(X)
print('Predict Time: ',datetime.now() - start_predict)

print('Maximum Error',np.max(np.abs(np.floor(preds) - y)))