import os
from tkinter.tix import Tree
import pandas as pd
from pyparsing import Regex
import src.db as db
import src.bot as bot
from tabulate import tabulate
import src.utils_bot as utils_bot
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Define project main path
main_path = os.getenv('MAIN_PATH')

query_path = os.path.join(os.getenv('MAIN_PATH'), 'queries/locksmiths')

LS_total_jobs_by_locksmith_day = open(os.path.join(query_path,
                    'LS_total_jobs_by_locksmith_day.txt'), 'r').read()

df = db.sql_to_df(LS_total_jobs_by_locksmith_day)

df = utils_bot.df_locksmith_to_str(df)
print(df)


