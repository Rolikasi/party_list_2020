#%%
import pandas as pd
import json
from collections import defaultdict
# %%
df = pd.read_csv('data/party_list.csv')
df = df.replace({'\n': ''}, regex=True)
df.rename(columns = {'Ф.А.А.' : 'name', 'Туулган датасы \nжана жылы': 'birth', 'Иштеген жери': 'work', 'Ээлеген кызматы': 'position', 'Саясий Партиясы': 'party'}, inplace=True)
df

# %%
def df_to_dict(df):
    if df.ndim == 1:
        return df.to_dict()

    ret = {}
    for key in df.index.get_level_values(0):
        sub_df = df.xs(key)
        ret[key] = df_to_dict(sub_df)
    return ret
# %%
df_to_dict(df)
# %%
df.groupby('Саясий Партиясы')
# %%
j = (df.groupby(['party'], as_index=True)
             .apply(lambda x: x[['name','birth', 'work', 'position', '№']].to_dict('r'))
             .reset_index()
             .rename(columns={0:'candidates'})
             .to_json(orient='records',force_ascii=False))
j
# %%
with open('data/party_list.json', 'w', encoding='utf8') as file:
    json.dump(j, file, ensure_ascii=False)
# %%
