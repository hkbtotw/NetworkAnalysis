import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime

pd.set_option('max_columns',50)
mpl.rcParams['lines.linewidth']=2


df1=pd.read_excel(r'C:\Users\70018928\Documents\Project 2019\Ad-hoc\Point System\TBPoint_Transaction_TC.xlsx',  sheet_name='Transaction_UA')
df= df1[['Id','L_Sender','Amount', 'ProjectId', 'Timestamp']].copy()
df['Timestamp'] =  pd.to_datetime(df['Timestamp'], format="%Y-%m-%d %H:%M:%S")
weeklist=[]
for n in df['Timestamp'].tolist():
    weeklist.append(datetime.strftime(n,'%W'))

df_dummy=pd.DataFrame(weeklist)
df_dummy.columns=['week_no']

df=pd.concat([df,df_dummy['week_no']],axis=1)

df.set_index('L_Sender', inplace=True)

df['CohortGroup'] = df.groupby(level=0)['week_no'].min()
df.reset_index(inplace=True)
grouped = df.groupby(['CohortGroup', 'week_no'])


# count the unique users, orders, and total revenue per Group + Period
cohorts = grouped.agg({'L_Sender': pd.Series.nunique})

# make the column names more meaningful
cohorts.rename(columns={'L_Sender': 'No_Sender'}, inplace=True)

#cohorts.tail()
#df.head()
def cohort_period(df):
    """
    Creates a `CohortPeriod` column, which is the Nth period based on the user's first purchase.
    
    Example
    -------
    Say you want to get the 3rd month for every user:
        df.sort(['UserId', 'OrderTime', inplace=True)
        df = df.groupby('UserId').apply(cohort_period)
        df[df.CohortPeriod == 3]
    """
    df['CohortPeriod'] = np.arange(len(df)) + 1
    return df

cohorts = cohorts.groupby(level=0).apply(cohort_period)

# reindex the DataFrame
cohorts.reset_index(inplace=True)
cohorts.set_index(['CohortGroup', 'CohortPeriod'], inplace=True)

cohorts.head()

# create a Series holding the total size of each CohortGroup
cohort_group_size = cohorts['No_Sender'].groupby(level=0).first()
cohort_group_size.head()


cohorts['No_Sender'].unstack(0).head()
user_retention = cohorts['No_Sender'].unstack(0).divide(cohort_group_size, axis=1)
user_retention.head(10)
user_retention[['27', '28', '29']].plot(figsize=(10,5))
plt.title('Cohorts : Repeated Sender')
plt.xticks(np.arange(1, 12.1, 1))
plt.xlim(1, 12)
plt.ylabel('% of Repeated Sender')


import seaborn as sns
sns.set(style='white')

plt.figure(figsize=(12, 8))
plt.title('Cohorts: Repeated Sender')
sns.heatmap(user_retention.T, mask=user_retention.T.isnull(), annot=True, fmt='.0%')

plt.show()

print(' --- Complete -----')