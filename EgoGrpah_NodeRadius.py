import pandas as pd
import networkx as nx
import pyodbc
import datetime


conn = pyodbc.connect('Driver={SQL Server};'
                        #'Server=SBNDCBIDSCIDB01;'
                        'Server=SBNDCTBVPOINT02;'
                        #'Database=TBL_ADHOC;'
                        'Database=TBPoint;'
                        'Trusted_Connection=yes;')



#sql="select cast   from [dbo].[Transaction]"
sql="SELECT cast(A.[Id] as varchar) as [Id],"\
      " cast(A.[Timestamp] as varchar) as [Timestamp],"\
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
FCT_TRNS['Timestamp']=FCT_TRNS['Timestamp'].astype(str)

#print(FCT_TRNS)
df1=FCT_TRNS


#----------------------------------------FCT_TRNS table for Networkx------------------------------------------------------------------------


#Get Transaction data to create Graph

df2_Transaction = df1[['L_Sender','L_Receiver', 'Amount', 'ProjectId', 'ReasonId', 'Timestamp']].copy()
df2_Transaction['Timestamp']=df2_Transaction['Timestamp'].astype(str)

_Pairs2=df2_Transaction[['L_Sender','L_Receiver', 'Amount']].values.tolist()

#Create Graph using Directed Graph :  NetworkX package
# Undirected graph for detecting connected community
g=nx.Graph()
g.add_weighted_edges_from(_Pairs2)






# Multi directed graph for creating actual network
GM=nx.MultiDiGraph()
#GM.add_weighted_edges_from(_Pairs2)

GM.add_nodes_from(df2_Transaction['L_Sender'])
GM.add_nodes_from(df2_Transaction['L_Receiver'])

for r,d in df2_Transaction.iterrows():
    GM.add_edge(d['L_Sender'], d['L_Receiver'], Amount=d['Amount'], ProjectId=d['ProjectId'], ReasonId=d['ReasonId'],date=d['Timestamp'])

#GM = nx.from_pandas_edgelist(df2_Transaction, 'L_Sender', 'L_Receiver', ['Amount', 'ProjectId', 'ReasonId'],create_using=GMC)


components = nx.connected_components(g)
Community=list(components)
NoCommunity=len(list(Community))
#print(' #Connected G : ', NoCommunity)
#print(' Community : ',Community[0], ' : ', Community[1])


count=1
GList=[]
dummy=[]
for i in Community:
    Guc=nx.MultiDiGraph()
    dummy.clear()
    # Multi directed graph for creating subgraph of connected community
    dummy=list(GM.subgraph(list(i)).edges(data=True))
    #print( ' dummy : ',dummy)
    Guc.add_weighted_edges_from(dummy, label=count)
    #print(' =>',list(i), ' : ',type(i), ' count: ', count)
    #for j in Guc.edges(data=True): 
    #    print(j) 

    dummy=list(Guc.edges.data())
    GList=GList+dummy
    count=count+1


dll=pd.DataFrame(GList)
dll.columns=['S','R','LB']
dll_2=dll['LB'].tolist()
ld = [d.get('label', None) for d in dll_2]
ld_w = [d.get('weight', None) for d in dll_2]
dll['GR']=pd.DataFrame(ld)
dll['LB']=pd.DataFrame(ld_w)

print(' dll : ',dll)

#Start computing Network Parameter by looping thru members of each community
D1=[]
D2=[]
D3=[]
D4=[]
D5=[]
for i in range(1,NoCommunity+1):
    dll_NC = dll[dll['GR'] == i]
    #print(' i : ',i,' Comm: ',Community[i-1])
    #print(' : ',i, ', ',dll_NC)
    D1=Community[i-1]
    #print(' i : ',i,' Comm: ',D1)
    D3=[]

    
    for n in D1:
    #_Pairs3=dll_NC[['S','R','LB']].values.tolist()
    #GM1=nx.MultiDiGraph()
    #GM2=nx.MultiGraph()
    #GM1.add_weighted_edges_from(_Pairs3)
    #GM2.add_weighted_edges_from(_Pairs3)
     #Create DiGraph object to get edge list of each ego graph
        g1=nx.MultiDiGraph()
        D3.clear()
        #Search with nx.ego_graph with radius=5 indicating the level of network depth
        #D3=list(nx.ego_graph(g, n, radius=1, undirected=True).edges(data=True))
        #D3=list(nx.ego_graph(GM, n, radius=3, undirected=True).edges(data=True))
        D3=list(nx.ego_graph(GM, n, radius=5, undirected=False).edges(data=True))
        g1.add_edges_from(D3, label=n, group=i)
        D3=list(g1.edges.data())
        
        for j in g1.nodes(data=True): 
            D4=[]
            #print(' j :: ', j[0], ' => ',n) 
            g1.node[j[0]]['radius']=nx.shortest_path_length(g1, source=n, target=j[0])
            g1.node[j[0]]['LB']=n
            g1.node[j[0]]['GR']=i
            #print(' radius :: ', g1.node[i[0]]['radius']) 
            D4=list(g1.node.data())

        D5=D5+D4   
        D2=D2+D3
    

dll=pd.DataFrame(D2)
dll.columns=['S','R','LB']

dll_4=dll['LB'].apply(pd.Series)
dll_4.columns=['EgoNode','Group','Weight', 'ProjectId', 'ReasonId', 'Date' ]
#print(dll_4)
dll['LB']=dll_4['EgoNode']
#dll=pd.concat([dll, dll_4['EgoNode']], axis=1)
dll=pd.concat([dll, dll_4['Weight']], axis=1)
dll=pd.concat([dll, dll_4['ReasonId']], axis=1)
dll=pd.concat([dll, dll_4['ProjectId']], axis=1)
dll=pd.concat([dll, dll_4['Group']], axis=1)
dll=pd.concat([dll, dll_4['Date']], axis=1)


print(dll)

dln=pd.DataFrame(D5)
print(' dln : ', dln)
dln.columns=['Node','LB']
print(dln)
dln_4=dln['LB'].apply(pd.Series)
dln_4.columns=['Radius','LB','GR']
print(dln_4)
dln=pd.concat([dln, dln_4['Radius']], axis=1)
dln=pd.concat([dln, dln_4['GR']], axis=1)
dln['LB']=dln_4['LB']
print(dln)


#------- Write New calculated data back to [TBL_ADHOC].[dbo].[TBP_EgoGraph]---------------------------

'''
conn1 = pyodbc.connect('Driver={SQL Server};'
                        'Server=SBNDCBIDSCIDB01;'
                         'Database=TBL_ADHOC;'
                         'Trusted_Connection=yes;')

#- Delete all records from the table
sql="""DELETE FROM TBL_ADHOC.dbo.TBP_EgoGraph"""

cursor=conn1.cursor()
cursor.execute(sql)
conn1.commit()

for index, row in dll.iterrows():
    cursor.execute("INSERT INTO TBL_ADHOC.dbo.TBP_EgoGraph([S],[R],[LB],[Weight],[ReasonId],[ProjectId],[Group],[Date]) values (?,?,?,?,?,?,?,?)", row['S'], row['R'], row['LB'], row['Weight'], row['ReasonId'], row['ProjectId'], row['Group'], row['Date'])
   

conn1.commit()


cursor.close()
conn1.close()

'''


#=========================================PBI Above, Below for Testing ===================================

#Write out to CSV for Visualization in PBI
filename='EgoNode_Radius.csv'
dln.to_csv(filename, encoding='utf-8', index=False)

#Write out to Check Time
localnow=datetime.datetime.now()
localnow_str=localnow.strftime('%Y-%m-%d %H:%M:%S')
output='Updated Time : '+' '+localnow_str


file1 = open(r"EgoRadiusLB_CheckTime.txt","w") 
L = output
file1.write("Hello \n") 
file1.writelines(L) 
file1.close() 

print(' --- DEV --- Complete --- ::  ',output)