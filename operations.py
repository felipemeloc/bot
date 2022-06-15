"""operations.py

Operation push bot for the hourly report of tasks/actions figures.
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
import src.utils_bot as utils_bot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Define project main path
main_path = os.getenv('MAIN_PATH')

# Define chat id
GROUP_ID = os.getenv('OPERATIONS_GROUP')

# For TEST
# GROUP_ID = os.getenv('TEST_GROUP')


################################## Query Load #####################################

query_path = os.path.join(os.getenv('MAIN_PATH'), 'queries\operations')

OPE_task_per_dep = open(os.path.join(query_path,
                    'OPE_task_per_dep.sql'), 'r').read()

OPE_total_task_closed_day = open(os.path.join(query_path,
                                'OPE_total_task_closed_day.sql'), 'r').read()


OPE_total_task_closed_hour = open(os.path.join(query_path,
                                        'OPE_total_task_closed_hour.sql'), 'r').read()

OPE_total_actions_completed_day = open(os.path.join(query_path,
            'OPE_total_actions_completed_day.sql'), 'r').read()

OPE_total_actions_completed_hour = open(os.path.join(query_path,
            'OPE_total_actions_completed_hour.sql'), 'r').read()

OPE_top_5 = open(os.path.join(query_path,
            'OPE_top.sql'), 'r').read()

def main():
    """Main function, it is in charge of:
    * Query the database
    * Transform dataframes to strings
    * Assemble report
    * Send report to Telegram
    """    
    date =  pd.Timestamp.now().strftime('%A, %d %B %H:%M')
    # Task Report queries to the database
    task1 = utils_bot.trans_one_row(db.sql_to_df(OPE_total_task_closed_day))
    task2 = utils_bot.trans_one_row(db.sql_to_df(OPE_total_task_closed_hour))
    task3 = utils_bot.df_to_str(db.sql_to_df(OPE_task_per_dep ))

    # Actions report queries to the database
    action1 = utils_bot.trans_one_row(db.sql_to_df(OPE_total_actions_completed_day))
    action2 = utils_bot.trans_one_row(db.sql_to_df(OPE_total_actions_completed_hour))
    action3 = utils_bot.df_to_str(db.sql_to_df(OPE_top_5 ), title='*Top 10 for Completed Actions*')
    operations_message = f"""{date}\n
*TASKS REPORT:*\n
{task1}
{task2}
{task3}\n
*ACTIONS REPORT:*\n
{action1}
{action2}
{action3}
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