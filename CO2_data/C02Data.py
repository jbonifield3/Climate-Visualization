import pandas as pd


start_year=1970
end_year=2013
maxlat=180
maxlon=360
root_path="C:/Users/dcarvall/Downloads/GRIDCAR/_/gridcar."

data=[]
for i in range(1,maxlat+1):
    for j in range(1,maxlon+1):
        data.append([i,j])

C02_df = pd.DataFrame(data, columns=['LAT', 'LONG'])


year=start_year
while year <= end_year:
    year_file = root_path + str(year)
    print(year_file)
    year_df = pd.read_csv(year_file, names=[str(year)], dtype={str(year):float})
    if len(year_df.index)==len(C02_df.index):
        C02_df=pd.concat([C02_df,year_df], axis=1)
    year=year+1

print(C02_df[:5])
C02_df.to_csv("CO2-data.csv")