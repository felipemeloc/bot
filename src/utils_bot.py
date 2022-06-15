"""
This is a custom module to adapt the format of the data to be printed on Telegram.

This module needs the installation of the following package:
* pandas: return a DataFrame object

Contains the following function:
* trans_one_row: Return string for total queries. Use:

    import utils_bot
    utils_bot.trans_one_row(df= YOUR_DATAFRAME)

* df_to_str: Return string for table; It can be added a title for the table. Use:

    import utils_bot
    utils_bot.df_to_str(df= YOUR_DATAFRAME,
                        title= 'YOUR TITLE')
"""

import pandas as pd
from tabulate import tabulate

def trans_one_row(df:pd.DataFrame)->str:
    """Function for convert a SQL query into a string to be printed in the chatbot.
    Function made for dataframes of shape (1,1).

    Args:
        df (pd.DataFrame): Dataframe of shape (1,1)

    Returns:
        str: string for total queries
    """    
    # Validate the dataframe shape
    if df.shape[0] == 1 and df.shape[1] == 1:
        df = df.reset_index(drop=True)
        key = df.columns[0]
        val = df.iloc[0,0]
        # Adapt information to be printed
        return f'*{key}*: {val}'
    else:
        print('The df should have a shape equal to (1, 1)')
        raise

def df_to_str(df:pd.DataFrame, title:str=None)->str:
    """Function for convert a SQL query into a string to be printed in the chatbot.
    Function made for dataframes of shape (n,2).

    Args:
        df (pd.DataFrame): Dataframe to be transformed. Dataframe of shape (n,2)
        title (str, optional): Table title. Defaults to None.

    Returns:
        str: return string for table
    """    
    # Validate the dataframe shape
    if df.shape[1] == 2:
        if title:
            # Set title added from user
            data =[title]
        else:
            # Set title from columns name
            data = [f'*{df.columns[1]} per {df.columns[0]}*']
        # Adapt information to be printed
        for _, row in df.iterrows():
            r = f'\t- {row[0]:<9}: {row[1]}'
            data.append(r)
        return '\n'.join(data)
    else:
        print('The df should have a shape equal to (n, 2)')
        raise

def df_staff_sales_to_str(o_df:pd.DataFrame)->str:
    df = o_df.copy()
    df['Name'] = df['Name'].str.slice(0,12)
    df['Amount'] = '£' + df['Amount'].astype(str)
    df_str = tabulate(df, showindex=False, headers=df.columns, tablefmt="prety", numalign='rigth')
    return df_str

def df_locksmith_to_str(o_df:pd.DataFrame)->str:
    df = o_df.copy()
    df['Locksmith'] = df['Locksmith'].str.lower().replace(r'wgtk[\s]*[\-]*', '', regex=True).str.replace(r'\(.*\)', '', regex=True).str.replace(r'[\s]+',' ',regex=True).str.strip().str.capitalize()
    df = df.groupby('Locksmith', as_index=False).sum().sort_values(df.columns[-1], ascending=False)
    str_df = df_to_str(df)
    return str_df

