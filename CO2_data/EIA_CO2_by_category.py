import pandas as pd
import numpy as np

url = "https://www.eia.gov/environment/emissions/state/excel/alabama.xlsx"
url ="https://www.eia.gov/environment/emissions/state/excel/coal_CO2_by_state_2016.xlsx"


categories = ['coal', 'commercial', 'electricity', 'industrial', 'natural_gas', 'petroleum', 'residential','transportation']
df_all = pd.DataFrame()

for cat in categories:
    url = "https://www.eia.gov/environment/emissions/state/excel/"+cat+"_CO2_by_state_2016.xlsx"
    print(url)
    df_temp = pd.read_excel(url, sheet_name='Sheet1', header=2, nrows =52) #51 rows pulls in all, not including United states, 52 pulls in US
    df_temp['category']=df_temp.State.apply(lambda x: cat)
    df_all = pd.concat([df_all, df_temp], axis=0, ignore_index=True)
    #print(df_all.shape)
    #print(df_all)
    del(df_temp)
#print(df_all.columns)
#print(df_all.head(-10))
#print(df_all.shape)
df_all.sort_values(by=['State'], inplace=True)

df_all.to_csv('CO2-Data-By-Category.csv', index=False)

#####################################################################################