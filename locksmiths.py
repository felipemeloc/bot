"""locksmiths.py

Locksmiths push bot for the hourly report of locksmiths jobs
The script preloads the txt files with each query. 
It uses the functions of the src.utils_bot module to modify the result of the queries. 
With the information, it generates the report and sends it to Telegram using the src.bot module.


The script needs the installation of the following packages:
* os: For path management and directory creation
* pandas: Return a DataFrame object
* dotenv: Load environment variables

This script uses the following custom modules:
* src: Adapt the format of the data to be printed on Telegram

"""
import os
import pandas as pd
import src.db as db
import src.bot as bot
from tabulate import tabulate
import src.utils_bot as utils_bot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Define project main path
main_path = os.getenv('MAIN_PATH')

# Define chat id
# GROUP_ID = os.getenv('LOCKSMITHS_GROUP')

# For TEST
GROUP_ID = os.getenv('TEST_GROUP')


################################## Query Load #####################################

query_path = os.path.join(os.getenv('MAIN_PATH'), 'queries/locksmiths')

LS_total_pending_jobs_by_locksmith_day = open(os.path.join(query_path,
                    'LS_total_pending_jobs_by_locksmith_day.sql'), 'r').read()

LS_total_pending_jobs_day = open(os.path.join(query_path,
                    'LS_total_pending_jobs_day.sql'), 'r').read()

LS_total_completed_jobs_by_locksmith_day = open(os.path.join(query_path,
                    'LS_total_completed_jobs_by_locksmith_day.sql'), 'r').read()

LS_total_completed_jobs_day = open(os.path.join(query_path,
                    'LS_total_completed_jobs_day.sql'), 'r').read()

LS_total_revenue_by_locksmith_day = open(os.path.join(query_path,
                    'LS_total_revenue_by_locksmith_day.sql'), 'r').read()

LS_total_revenue_day = open(os.path.join(query_path,
                    'LS_total_revenue_day.sql'), 'r').read()


def main():
    """Main function, it is in charge of:
    * Query the database
    * Transform dataframes to strings
    * Assemble report
    * Send report to Telegram
    """    
    date =  pd.Timestamp.now().strftime('%A, %d %B %H:%M')
    # Today's Pending Jobs
    locksmiths_jobs_pending = utils_bot.df_locksmith_to_str( db.sql_to_df(LS_total_pending_jobs_by_locksmith_day))
    total_jobs_pending = utils_bot.trans_one_row(db.sql_to_df(LS_total_pending_jobs_day))

    # Today's Completed Jobs
    locksmiths_jobs_completed = utils_bot.df_locksmith_to_str( db.sql_to_df(LS_total_completed_jobs_by_locksmith_day))
    total_jobs_completed = utils_bot.trans_one_row(db.sql_to_df(LS_total_completed_jobs_day))

    # Today's Revenue 
    locksmiths_revenue = utils_bot.df_locksmith_to_str( db.sql_to_df(LS_total_revenue_by_locksmith_day), money_col='Revenue')
    total_revenue = utils_bot.trans_one_row(db.sql_to_df(LS_total_revenue_day), money=True)
    
    operations_message = f"""{date}\n
*TODAY'S PENDING JOBS:*\n
{locksmiths_jobs_pending}\n
{total_jobs_pending}\n
*TODAY'S COMPLETED JOBS:*\n
{locksmiths_jobs_completed}\n
{total_jobs_completed}\n
*TODAY'S REVENUE:*\n
{locksmiths_revenue}\n
{total_revenue}\n
"""
    print('-'*60,'\n',operations_message,'-'*60)
    bot.send_message(GROUP_ID, operations_message)

if __name__ == '__main__':
    try:
        NOW = pd.Timestamp.now()
        print(NOW)
        hour = NOW.hour
        print('Bot online')
        # Time validation to check if the hour is between 6 and 21
        if hour >= 6 and hour <= 21:
            main()
            print('Process Successful')
        else:
            print('Execution after hours')
    except Exception as e:
        print(e)