import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import pyodbc
import datetime


#Record Start time
localnow=datetime.datetime.now()
localnow_str=localnow.strftime('%Y-%m-%d %H:%M:%S')
StartTime='StartTime : '+' '+localnow_str
'''
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

'''
#----------------------------------------FCT_TRNS table for Networkx------------------------------------------------------------------------
df1=pd.read_excel(r'C:\Users\70018928\Documents\Project 2019\Ad-hoc\Point System\TBPoint_Transaction_TC.xlsx',  sheet_name='Transaction_UB')


#------------------------------------------------------------------------------

df2_Transaction = df1[['L_Sender','L_Receiver', 'Amount', 'ProjectId', 'ReasonId', 'Timestamp']].copy()

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

#print(' dll : ',dll)

#Start computing Network Parameter by looping thru members of each community
D1=[]
D2=[]
D3=[]

#Color coded radius
D4=[]
D5=[]

#Level

LEV1=[]
LEV2=[]
D6=[]
D7=[]

LEV3=[]
LEV4=[]

LEV5=[]
LEV6=[]
LEV7=[]

#for i in range(1,NoCommunity+1):
i=1
if i==1 :
    dll_NC = dll[dll['GR'] == i]
    #print(' i : ',i,' Comm: ',Community[i-1])
    print(' : ',i, ', ',dll_NC)
    
    # Choose only on node to generate the personal network to reduce calculation time
    #D1=Community[i-1]
    D1=['L11018667','L11034982','L11004281','L11024263','L11032745']
    
    
    print(' i : ',i,' Comm: ',D1)
    D3=[]
    D6=[]


    for n in D1:
    #_Pairs3=dll_NC[['S','R','LB']].values.tolist()
    #GM1=nx.MultiDiGraph()
    #GM2=nx.MultiGraph()
    #GM1.add_weighted_edges_from(_Pairs3)
    #GM2.add_weighted_edges_from(_Pairs3)
     #Create DiGraph object to get edge list of each ego graph
        g1=nx.MultiDiGraph()
        g2=nx.Graph()
        D3.clear()
        D6.clear()
        #Search with nx.ego_graph with radius=5 indicating the level of network depth
        #D3=list(nx.ego_graph(g, n, radius=1, undirected=True).edges(data=True))
        D3=list(nx.ego_graph(GM, n, radius=4, undirected=False).edges(data=True))
        g1.add_edges_from(D3, label=n, group=i)
        g2.add_edges_from(D3, label=n, group=i)
        D3=list(g1.edges.data())

        #print(' =>>>> i : ',list(g1.edges.data()),'  ::::   ',list(g2.edges.data()))

        # Color coded node by radius
        for j in g2.nodes(data=True): 
            D4=[]
            #print(' j :: ', j[0], ' => ',n) 
            g2.node[j[0]]['radius']=nx.shortest_path_length(g2, source=n, target=j[0])
            g2.node[j[0]]['LB']=n
            g2.node[j[0]]['GR']=i
            #print(' i : ',i,' :: n ',n)
            #print(' radius :: ', g1.node[j[0]]['radius']) 
            D4=list(g2.node.data(data=True))

        
        LEV1.clear()
        LEV2.clear()
        LEV3.clear()
        LEV4.clear()
        LEV5.clear()
        LEV6.clear()
        LEV7.clear()
        #print(' D4 : ', D4)
        LEV1=LEV1+ list(n for n,v in D4 if v['radius'] == 1) 
        #print(' LEV :: ', list(LEV1), ' , ', list(LEV2))
        gnew=nx.DiGraph()


        # Calculate Forward path
        for k in LEV1:
            [gnew.add_edge(n,k,LB=n, radius=1, weight=w) for u,v,w in g1.edges.data() if(u==n) and (v==k)]  
        
        
        LEV1=LEV1+ list(n for n,v in D4 if v['radius'] == 2 )
            #print('  edge : ',gnew.edges.data())
        for g in LEV1:
            for f in LEV2:
                #[print(' g: ',g,', f: ',f,' :: e:',u,':',v,':',w) for u,v,w in g1.edges.data() ]
                [gnew.add_edge(g,f,LB=n,radius=2, weight=w) for u,v,w in g1.edges.data() if(g==u) and (f==v)]    
                #for u,v,w in g1.edges.data():
                 #   if(g==u) and (f==v):
                 #       gnew.add_edge(g,f,LB=n,radius=2, weight=w)
                 #       print(' g : ',g, ' and ', f )
                 #       nodes_1.append(f)


            #print('  edge : ',gnew.edges.data())
        #D6=list(gnew.edges.data())
        #print('  D6  :   ', D6)
             
        LEV2=LEV1+ list(n for n,v in D4 if v['radius'] == 3 )
        for g in LEV2:
            for f in LEV3:
                #[print(' g: ',g,', f: ',f,' :: e:',u,':',v,':',w) for u,v,w in g1.edges.data() ]
                [gnew.add_edge(g,f,LB=n,radius=3, weight=w) for u,v,w in g1.edges.data() if(g==u) and (f==v)]     
            #print('  edge : ',gnew.edges.data())
        #D6=list(gnew.edges.data())
        #print('  D6  :   ', D6)
        
        LEV3=LEV2+ list(n for n,v in D4 if v['radius'] == 4 )
        for g in LEV3:
            for f in LEV4:
                #[print(' g: ',g,', f: ',f,' :: e:',u,':',v,':',w) for u,v,w in g1.edges.data() ]
                [gnew.add_edge(g,f,LB=n,radius=4, weight=w) for u,v,w in g1.edges.data() if(g==u) and (f==v)]     
            #print('  edge : ',gnew.edges.data())
        #D6=list(gnew.edges.data())
        #print('  D6  :   ', D6)
             
        LEV4=LEV3+ list(n for n,v in D4 if v['radius'] == 5 )
        for g in LEV4:
            for f in LEV5:
                #[print(' g: ',g,', f: ',f,' :: e:',u,':',v,':',w) for u,v,w in g1.edges.data() ]
                [gnew.add_edge(g,f,LB=n,radius=5, weight=w) for u,v,w in g1.edges.data() if(g==u) and (f==v)]     
            #print('  edge : ',gnew.edges.data())
        #D6=list(gnew.edges.data())
        #print('  D6  :   ', D6)



        LEV5=LEV4+ list(n for n,v in D4 if v['radius'] == 6 )
        for g in LEV5:
            for f in LEV6:
                #[print(' g: ',g,', f: ',f,' :: e:',u,':',v,':',w) for u,v,w in g1.edges.data() ]
                [gnew.add_edge(g,f,LB=n,radius=6, weight=w) for u,v,w in g1.edges.data() if(g==u) and (f==v)]     
            #print('  edge : ',gnew.edges.data())
        #D6=list(gnew.edges.data())
        #print('  D6  :   ', D6)
        
        LEV6=LEV5+ list(n for n,v in D4 if v['radius'] == 7 )
        for g in LEV6:
            for f in LEV7:
                #[print(' g: ',g,', f: ',f,' :: e:',u,':',v,':',w) for u,v,w in g1.edges.data() ]
                [gnew.add_edge(g,f,LB=n,radius=7, weight=w) for u,v,w in g1.edges.data() if(g==u) and (f==v)]     
            #print('  edge : ',gnew.edges.data())
    


        D6=list(gnew.edges.data())     
        #print('  D6  :   ', D6)

        D7=D7+D6
        
        D5=D5+D4  
        D2=D2+D3
    

dego=pd.DataFrame(D7)
dego.columns=['S','R','LB']
print(' dego : ', dego)
dego_4=dego['LB'].apply(pd.Series)
dego_4.columns=['EgoNode','radius','weight' ]
dego_5=dego_4['weight'].apply(pd.Series)
dego_5.columns=['Label','Group','amount',  'ProjectId', 'ReasonId','Timestamp' ]
print(' dego 5 : ', dego_5)
dego_4['weight']=dego_5['amount']
dego_4=pd.concat([dego_4, dego_5['Label']], axis=1)
dego_4=pd.concat([dego_4, dego_5['Group']], axis=1)
dego_4=pd.concat([dego_4, dego_5['ReasonId']], axis=1)
dego_4=pd.concat([dego_4, dego_5['Timestamp']], axis=1)
dego_4=pd.concat([dego_4, dego_5['ProjectId']], axis=1)
print(' dego 4 : ',dego_4)

dego['LB']=dego_4['Label']
dego=pd.concat([dego, dego_4['radius']], axis=1)
dego=pd.concat([dego, dego_4['weight']], axis=1)
dego=pd.concat([dego, dego_4['Group']], axis=1)
dego=pd.concat([dego, dego_4['ReasonId']], axis=1)
dego=pd.concat([dego, dego_4['Timestamp']], axis=1)
dego=pd.concat([dego, dego_4['ProjectId']], axis=1)
print(' dego : ',dego)


#------- Write New calculated data back to [TBL_ADHOC].[dbo].[TBP_EgoGraph]---------------------------

'''
conn1 = pyodbc.connect('Driver={SQL Server};'
                        'Server=SBNDCBIDSCIDB01;'
                         'Database=TBL_ADHOC;'
                         'Trusted_Connection=yes;')

#- Delete all records from the table
sql="""DELETE FROM TBL_ADHOC.dbo.TBP_EgoGraph_2"""

cursor=conn1.cursor()
cursor.execute(sql)
conn1.commit()

for index, row in dego.iterrows():
    cursor.execute("INSERT INTO TBL_ADHOC.dbo.TBP_EgoGraph_2([S],[R],[LB],[radius],[weight],[Group],[ReasonId],[Timestamp],[ProjectId]) values (?,?,?,?,?,?,?,?,?)", row['S'], row['R'], row['LB'], row['radius'],row['weight'], row['Group'], row['ReasonId'], row['Timestamp'], row['ProjectId'])
   

conn1.commit()


cursor.close()
conn1.close()


'''

#=========================================PBI Above, Below for Testing ===================================


#Write out to CSV for Visualization in PBI
filename='EgoGraph_Lean_20190730.csv'
dego.to_csv(filename, encoding='utf-8', index=False)
#dll.to_csv(filename, encoding='utf-8', index=False)

#Write out to Check Time
localnow=datetime.datetime.now()
localnow_str=localnow.strftime('%Y-%m-%d %H:%M:%S')
output='Updated Time : ',StartTime,' + ', localnow_str

print(' ------ Comnplete ----- :: ', output)

