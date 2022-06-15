import src.db as db
# path = 'queries\locksmiths\LS_total_completed_jobs_by_locksmith_day.sql'
path = 'queries\locksmiths\LS_total_pending_jobs_by_locksmith_day.sql'

with open(path, 'r') as f:
    data = f.read()

o_df = db.sql_to_df(data)


print('-*-'*30)
print('Original')
print(o_df)
print('-*-'*30)



df = o_df.copy()
 
df['Locksmith'] = df['Locksmith'].str.lower().replace(r'wgtk[\s]*[\-]*', '', regex=True).str.replace(r'\(.*\)', '', regex=True).str.replace(r'[\s]+',' ',regex=True).str.strip().str.capitalize()

df = df.groupby('Locksmith', as_index=False).sum().sort_values(df.columns[-1], ascending=False)

print('-*-'*30)
print('Fix')
print(df)
print('-*-'*30)


