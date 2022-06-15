import src.db as db
path = 'queries/locksmiths/test.sql'

with open(path, 'r') as f:
    data = f.read()

print(data)

df = db.sql_to_df(data)

print(df)


