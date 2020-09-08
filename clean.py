#%%
import pandas as pd
import json
from datetime import date
from collections import OrderedDict
# %%
def calculateAge(birthDate):

    today = date.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
    if (age % 10) >= 5 or (age % 10) == 0:
        return str(age) + ' лет'
    elif (age % 10) == 1:
        return str(age) + ' год'
    else:
        return str(age) + ' года'
# %%

df = pd.read_csv('data/party_list.csv')
df = df.replace({'\n': ''}, regex=True)
df.rename(columns = {'Ф.А.А.' : 'name', 'Туулган датасы \nжана жылы': 'years', 'Иштеген жери': 'work', 'Ээлеген кызматы': 'position', 'Саясий Партиясы': 'party'}, inplace=True)
df.years = df.years.replace({r'(\d\d\.\d\d)\.(\d\d$)': r'\1.19\2'}, regex=True)
df.years = pd.to_datetime(df['years'], format='%d.%m.%Y')
df.years = df.years.apply(calculateAge)
df.party = df.party.replace({'«': '', '»': '', '"': '', '“': ''}, regex=True)
df
# %%
j = (df.groupby(['party'], as_index=True)
             .apply(lambda x: x[['№', 'name','years', 'work', 'position']].to_dict('r'))
             .reset_index()
             .rename(columns={0:'candidates'})
             .to_json(orient='records',force_ascii=False))
j
sort = sorted(json.loads(j), key=lambda k: len(k['party']) > 22, reverse=False)

# %%
with open('data/party_list.json', 'w', encoding='utf8') as file:
    json.dump(sort, file, ensure_ascii=False)
# %%
type(j)
# %%
sort
# %%
