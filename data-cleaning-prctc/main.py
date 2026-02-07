import pandas as pd

df = pd.read_csv('cafeSales.csv')

print(pd.DataFrame(df.to_dict()))   