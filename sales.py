"""sales.py

Sales push bot for the hourly report of sales figures
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
GROUP_ID = os.getenv('SALES_GROUP')

# For TEST
# GROUP_ID = os.getenv('TEST_GROUP')


################################## Query Load #####################################

query_path = os.path.join(os.getenv('MAIN_PATH'), 'queries/sales')

SL_company_conversion_day = open(os.path.join(query_path,
                    'SL_company_conversion_day.sql'), 'r').read()

SL_total_conversion_day = open(os.path.join(query_path,
                    'SL_total_conversion_day.sql'), 'r').read()

SL_company_conversion_hour = open(os.path.join(query_path,
                    'SL_company_conversion_hour.sql'), 'r').read()

SL_total_conversion_hour = open(os.path.join(query_path,
                    'SL_total_conversion_hour.sql'), 'r').read()

SL_staff_day = open(os.path.join(query_path,
                    'SL_staff_day.sql'), 'r').read()


SL_staff_hour= open(os.path.join(query_path,
                    'SL_staff_hour.sql'), 'r').read()


def main():
    """Main function, it is in charge of:
    * Query the database
    * Transform dataframes to strings
    * Assemble report
    * Send report to Telegram
    """    
    date =  pd.Timestamp.now().strftime('%A, %d %B %H:%M')
    # Today's conversion Report queries to the database
    today1 = utils_bot.df_to_str(db.sql_to_df(SL_company_conversion_day))
    today2 = utils_bot.trans_one_row(db.sql_to_df(SL_total_conversion_day))

    # Hour conversion Report queries to the database
    hour1 = utils_bot.df_to_str(db.sql_to_df(SL_company_conversion_hour))
    hour2 = utils_bot.trans_one_row(db.sql_to_df(SL_total_conversion_hour))

    # Staff Sales
    staff1 = db.sql_to_df(SL_staff_day)
    staff1 = utils_bot.df_staff_sales_to_str(staff1)
    staff2 = db.sql_to_df(SL_staff_hour)
    staff2 =  utils_bot.df_staff_sales_to_str(staff2)
    operations_message = f"""{date}\n
*TODAY'S CONVERSION:*\n
{today1}\n
{today2}\n
\n*HOUR CONVERSION:*\n
{hour1}\n
{hour2}\n
\n*STAFF SALES:*\n
*Today's Sales*
{staff1}\n
*Hour Sales*
{staff2}
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