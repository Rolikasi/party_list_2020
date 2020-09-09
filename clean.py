# %%
import pandas as pd
import json
from datetime import date
from collections import OrderedDict
# %%


def calculateAge(birthDate):

    today = date.today()
    age = today.year - birthDate.year - \
        ((today.month, today.day) < (birthDate.month, birthDate.day))
    if (age % 10) >= 5 or (age % 10) == 0:
        return str(age) + ' жашта' #лет
    elif (age % 10) == 1:
        return str(age) + ' жашта' #год
    else:
        return str(age) + ' жашта' #года


col_replace = {'Ф.А.А.': 'name', 'Туулган датасы \nжана жылы': 'years',
               'Иштеген жери': 'work', 'Ээлеген кызматы': 'position', 'Саясий Партиясы': 'party',
               'Ф.И.О.': 'name',
               'Дата рождения': 'years',
               'Место работы': 'work',
               'Должность': 'position',
               'Партия': 'party'}
# %%
df = pd.read_csv('data/party_list_kg.csv')
df = df.replace({'\n': ''}, regex=True)
df.rename(columns=col_replace, inplace=True)
df.years = df.years.replace({r'(\d\d\.\d\d)\.(\d\d$)': r'\1.19\2'}, regex=True)
df.years = pd.to_datetime(df['years'], format='%d.%m.%Y')
df.years = df.years.apply(calculateAge)
df.party = df.party.replace({'«': '', '»': '', '"': '', '“': ''}, regex=True)
df['description'] = df[['work', 'position']].apply(
    lambda x: ', '.join(x.astype(str)), axis=1)
df.description = df.description.replace({', nan': '', 'nan,': ''}, regex=True)
df.description = df.description.replace({r'(.*)\s?-\s?$': r'\1'}, regex=True)
df.description = df.description.str.strip()
df.drop(['work', 'position'], 1, inplace=True)
df
# %%
j = (df.groupby(['party'], as_index=True)
     .apply(lambda x: x[['№', 'name', 'years', 'description']].to_dict('r'))
     .reset_index()
     .rename(columns={0: 'candidates'})
     .to_json(orient='records', force_ascii=False))
j
sort = sorted(json.loads(j), key=lambda k: len(k['party']) > 22, reverse=False)

# %%
with open('data/party_list_kg.json', 'w', encoding='utf8') as file:
    json.dump(sort, file, ensure_ascii=False)
# %%
type(j)
# %%
sort
# %%
df.info()
# %%
