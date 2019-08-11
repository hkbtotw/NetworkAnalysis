import pandas as pd
import pprint
#from WordCut_Lemmatized import Processing
#from WordCut_Lemmatized import TopicModeling
from WordCut_Lemmatized_pythainlp import Processing
from WordCut_Lemmatized_pythainlp import TopicModeling


# Read in input from Excel Spreadsheet
xls = pd.ExcelFile(r'C:\Users\kira\Downloads\TBPoint_Transaction_TC.xlsx')

df1 = pd.read_excel(xls, 'Transaction_NLP')
df2_Transaction = df1[['Id','OtherReason']].copy()
#df_Filtered_df2=df2_Transaction.dropna()
df_Filtered_df2=df2_Transaction
df2_Transaction['OtherReason']=df2_Transaction['OtherReason'].astype(str)
E1=df_Filtered_df2[['OtherReason']].values.tolist()

# Call  WordCut and Stopword removal
Lemma=Processing(E1)
print(' lemma : ', Lemma, '  ::  ', type(Lemma))


# Call TopicModeling by LDA

lda=TopicModeling(Lemma)

pp=pprint.PrettyPrinter(indent=4)

num_words=8
pp.pprint(lda.print_topics(num_words=num_words))
