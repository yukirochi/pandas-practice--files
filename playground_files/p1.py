import pandas as pd

df = pd.read_csv('wuwa.csv')
#print(df.head(3)) # return the first 3
#print(df.tail(3)) # return the last 3
var = df.to_dict
#print(df)
#print(pd.DataFrame(df.to_string))
d = {
    "a":1,
    "b":2,
    "c":3
}

#print(pd.Series(d, index = ["d"]))

a = [[1,2],[2],[2,4,5]]

b = pd.Series(a, index = ['q','w','d'])  #index should have the same length as the list



#print(pd.DataFrame(pd.Series(b, index = ['q','w','d'])).loc['q'])
