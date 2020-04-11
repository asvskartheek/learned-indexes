# Inspired from https://github.com/yangjufo/Learned-Indexes/

import numpy as np
import pandas as pd

DATA_SIZE = 100_000 # Number of data points
BLOCK_SIZE = 100 # Number of points in each block
file_name = "exponential.csv" # Dest. Data file

multiplicant = 10_000_000 # WHY!?
data = np.random.exponential(10, DATA_SIZE) # Distribution of data points
data.sort()
df = pd.DataFrame()
df['key'] = (data*multiplicant).astype(int)
df['value'] = np.ones(df.shape[0]).astype(int) # init
for index,row in df.iterrows():
    row['value'] = int(index//BLOCK_SIZE)

df.to_csv(file_name,index=False)