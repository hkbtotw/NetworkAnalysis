import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.pyplot import yticks
from datetime import datetime


pd.set_option('max_columns',50)
mpl.rcParams['lines.linewidth']=2

#%matplotlib inline

df1=pd.read_excel(r'C:\Users\70018928\Documents\Project 2019\Ad-hoc\Point System\TBPoint_Transaction_TC.xlsx',  sheet_name='Transaction_UB')


df= df1[['Id','L_Sender','Amount', 'ProjectId', 'Timestamp']].copy()
df['Timestamp'] =  pd.to_datetime(df['Timestamp'], format="%Y-%m-%d")
daylist=[]
for n in df['Timestamp'].tolist():
    daylist.append(datetime.strftime(n,'%d'))

df_dummy=pd.DataFrame(daylist)
df_dummy.columns=['day_no']

df=pd.concat([df,df_dummy['day_no']],axis=1)



df.set_index('L_Sender', inplace=True)


df['CohortGroup'] = df.groupby(level=0)['day_no'].min()
df.reset_index(inplace=True)

df['CohortPeriod']=df['day_no'].astype(int)-df['CohortGroup'].astype(int)+1


print(df)

grouped = df.groupby(['CohortGroup', 'day_no', 'CohortPeriod'])


# count the unique users, orders, and total revenue per Group + Period
cohorts = grouped.agg({'L_Sender': pd.Series.nunique})

# make the column names more meaningful
cohorts.rename(columns={'L_Sender': 'No_Sender'}, inplace=True)




#print(cohorts)
cohorts.reset_index(inplace=True)
cohorts.set_index(['CohortGroup', 'CohortPeriod'], inplace=True)

cohorts.head()

# create a Series holding the total size of each CohortGroup
cohort_group_size = cohorts['No_Sender'].groupby(level=0).first()
cohort_group_size.head()


cohorts['No_Sender'].unstack(0).head()
user_retention = cohorts['No_Sender'].unstack(0).divide(cohort_group_size, axis=1)
user_retention.head(10)



user_retention.plot(figsize=(10,5))
plt.title('Cohorts : Repeated Sender')
plt.xticks(np.arange(1, 26.1, 1))
plt.xlim(1, 19)
plt.ylabel('% of Repeated Sender')
plt.legend(loc='best', fontsize = 'small')
#L=plt.legend()
#L.get_texts()[0].set_text('1st week')
#L.get_texts()[1].set_text('2nd week')
#L.get_texts()[2].set_text('3rd week');


import seaborn as sns
sns.set(style='white')

plt.figure(figsize=(14, 10))
plt.title('Cohorts: Repeated Sender')

yticklabels = range(1, 22, 1)
# the index position of the tick labels
yticks = []
count=1
for label in yticklabels:
    idx_pos = count
    count=count+1
    yticks.append(idx_pos)

xticklabels = range(1, 22, 1)
# the index position of the tick labels
xticks = []
count=1
for label in xticklabels:
    idx_pos = count
    count=count+1
    xticks.append(idx_pos)

ax1=sns.heatmap(user_retention.T, mask=user_retention.T.isnull(), annot=True, fmt='.0%',xticklabels=xticklabels,yticklabels=yticklabels, cbar=True,cbar_kws={"shrink": .82})
ax1.set_yticks(yticks,  "center")
plt.show();

