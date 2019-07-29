import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import pyodbc
import datetime
from datetime import datetime

'''
# Option 1 : Read in data from Database

conn = pyodbc.connect('Driver={SQL Server};'
                        #'Server=SBNDCBIDSCIDB01;'
                        'Server=SBNDCTBVPOINT02;'
                        #'Database=TBL_ADHOC;'
                        'Database=TBPoint;'
                        'Trusted_Connection=yes;')



#sql="select cast   from [dbo].[Transaction]"
sql="SELECT cast(A.[Id] as varchar) as [Id],"\
      " A.[Timestamp],"\
      " concat('L',A.[Sender]) as L_Sender,"\
      " concat('L',A.[Receiver]) as L_Receiver,"\
      " cast(A.[Sender] as varchar) as [Sender],"\
      " cast(A.[Receiver] as varchar) as [Receiver],"\
      " A.[Amount], A.[ProjectId],"\
      " A.[ReasonId]"\
      "  from [dbo].[Transaction] A  "\
      "where "\
      "A.Sender not like 'TBTEMP%'  "\
      "and A.Sender <> '1'"\
      "and A.Receiver not like 'TBTEMP%' "\
      "and A.ProjectId not in "\
	   "  (select [Id] from [TBPoint].[dbo].[Project]"\
	   "	where [Id]  in (56) or AssignTo  like 'TBTEMP%' ) "\
    "order by Id "


FCT_TRNS = pd.read_sql(sql,conn)
conn.close()

FCT_TRNS['Id']=FCT_TRNS['Id'].astype(str)
FCT_TRNS['Sender']=FCT_TRNS['Sender'].astype(str)
FCT_TRNS['Receiver']=FCT_TRNS['Receiver'].astype(str)
#FCT_TRNS['Timestamp']=FCT_TRNS['Timestamp'].astype(str)

print(FCT_TRNS)
df1=FCT_TRNS
'''

#--------------------------------------------------------
# Option 2 : Read data in from spreadsheet

xls = pd.ExcelFile(r'C:\Users\kira\Downloads\TBPoint_Transaction_TC.xlsx')

#-----------------------------------------------------------
#Get Transaction data to create Graph

df1 = pd.read_excel(xls, 'Transaction_UA')


#======================================================================

df= df1[['Id','L_Sender','L_Receiver', 'Amount', 'ProjectId', 'ReasonId', 'Timestamp']].copy()
print('  df :  ',df1.info())
#df['Timestamp']=df.Timestamp.apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))

df['Timestamp'] =  pd.to_datetime(df['Timestamp'], format="%Y-%m-%d %H:%M:%S")
print( '  df : ', df, '  => ', type(df['Timestamp'][0]))

weeklist=[]
for n in df['Timestamp'].tolist():
    weeklist.append(datetime.strftime(n,'%W'))

df_dummy=pd.DataFrame(weeklist)
df_dummy.columns=['weeklist']

df=pd.concat([df,df_dummy['weeklist']],axis=1)

#print(' df : ', df['weeklist'])

weeklist=list(set(weeklist))

wkl1=['27']
wkl2=['28']
wkl3=['29']
print(' WL : ', weeklist, ' => ',wkl1,' :: ',wkl2,' :::: ',len(weeklist))

#Joint list to find Sender list
FList=df['L_Sender'].tolist()
D_Sender = list(set(FList))
print(' F : ',len(FList), '  =>  ',' D : ',len(D_Sender))

Cohort1=[]
dummy=[]
count=0
#D_Sender=['L11000236']
for n in D_Sender:
    #print(' Sender : ', n)
    dummy=[]
    count=0
    for k in wkl1:
          for i,j in df.iterrows():
              #print(' n : ', n, ' :: ', j['L_Sender'], ' => ',k,'----',j['weeklist'],' ::: ',count)
              if (n==j['L_Sender']) and (k==j['weeklist']):
                 count=count+1
                #print(' count : ',count,' =>', n)
    if count>0:       
        Cohort1.append(n)    
       

print(Cohort1, ', len : ', len(Cohort1))

#Search number left on week 2
Cohort1_wk2=[]
dummy=[]
count=0
#D_Sender=['L11000236']
for n in Cohort1:
    #print(' Sender : ', n)
    dummy=[]
    count=0
    for k in wkl2:
          for i,j in df.iterrows():
              #print(' n : ', n, ' :: ', j['L_Sender'], ' => ',k,'----',j['weeklist'],' ::: ',count)
              if (n==j['L_Sender']) and (k==j['weeklist']):
                 count=count+1
                #print(' count : ',count,' =>', n)
    if count>0:       
        Cohort1_wk2.append(n)    
       

print(Cohort1_wk2, ', len : ', len(Cohort1_wk2))

#Search number left on week 2
Cohort1_wk3=[]
dummy=[]
count=0
#D_Sender=['L11000236']
#for n in Cohort1_wk2:
for n in Cohort1:
    #print(' Sender : ', n)
    dummy=[]
    count=0
    for k in wkl3:
          for i,j in df.iterrows():
              #print(' n : ', n, ' :: ', j['L_Sender'], ' => ',k,'----',j['weeklist'],' ::: ',count)
              if (n==j['L_Sender']) and (k==j['weeklist']):
                 count=count+1
                #print(' count : ',count,' =>', n)
    if count>0:       
        Cohort1_wk3.append(n)    
       

print(Cohort1_wk3, ', len : ', len(Cohort1_wk3))