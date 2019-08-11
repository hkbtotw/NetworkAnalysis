import deepcut
import pythainlp
import pandas as pd
from deepcut import stop_words
from pythainlp.corpus import stopwords as thaisw
from nltk.corpus import stopwords as engsw
from pythainlp import word_tokenize as thai_tokens
from nltk import word_tokenize as eng_tokens

from nltk.stem import WordNetLemmatizer
from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel
import pprint

#outcome=deepcut.tokenize('ตัดคำได้ดีมาก')


ThaiWord_Deepcut=list(stop_words.THAI_STOP_WORDS)
ThaiWord=list(thaisw.words('thai'))
#print(' Thaiwords : ', ThaiWord)
EngWord=list(set(engsw.words('english')))
#print(' ew : ',EngWord, ' : ', type(EngWord))
Morewords=['การ','การทำงาน','ทำงาน','เสมอ','krub','Test', 'nan', ' ','test','.',',']
All_Stop_Word=ThaiWord_Deepcut+ThaiWord+EngWord+Morewords
#print(' ALL : ',All_Stop_Word)




xls = pd.ExcelFile(r'C:\Users\kira\Downloads\TBPoint_Transaction_TC.xlsx')

df1 = pd.read_excel(xls, 'Transaction_NLP')
df2_Transaction = df1[['Id','OtherReason']].copy()
#df_Filtered_df2=df2_Transaction.dropna()

df_Filtered_df2=df2_Transaction
df2_Transaction['OtherReason']=df2_Transaction['OtherReason'].astype(str)
E1=df_Filtered_df2[['OtherReason']].values.tolist()

EntryList=[]
for n in E1:
   # check=detect(n[0])   # th or en
    #print(' text : ', n[0], ' :: ',check)
    EntryList.append(n[0])

    #print(' EntryList : ', EntryList)

    Outcome=[]
for r in EntryList:
    Dummy=[]
    tokens=[]
    tokens=list(eng_tokens(r))
    lowered = [t.lower() for t in tokens]
    #print(' Dummy : ',lowered)
    lowered=" ".join(lowered)
    #Dummy=list(thai_tokens(lowered, engine='newmm'))
    Dummy=deepcut.tokenize(lowered,custom_dict=['ไทยเบฟ'])
    #print(' Dummy 2 : ',Dummy)
    Outcome.append(Dummy)

#print(' Outcome : ',Outcome, ' : ', len(Outcome))


NoStop=[]
for n in Outcome:
    Dummy=[]
    Dummy=[word for word in n if word not in All_Stop_Word]
    NoStop.append(Dummy)

print(' No stop : ',NoStop, ' len: ',len(NoStop))


# Instantiate the WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

# Lemmatize all tokens into a new list: lemmatized

Lemma=[]
for n in NoStop:
    Dummy=[]
    Dummy = [wordnet_lemmatizer.lemmatize(t) for t in n]
    Lemma.append(Dummy)

#print(' lemma : ', Lemma, '  ::  ', type(Lemma))


# Create a Dictionary from the articles: dictionary
dictionary = Dictionary(Lemma)

#print(' dict : ', dictionary)
 
# Create a MmCorpus: corpus
corpus = [dictionary.doc2bow(article) for article in Lemma]

# Print the first 10 word ids with their frequency counts from the fifth document
print(corpus, '  LEN  :  ', len(corpus))


num_topics=5
num_words=8
passes=20

lda=LdaModel(corpus, id2word=dictionary, num_topics=num_topics, passes=passes)

pp=pprint.PrettyPrinter(indent=4)

pp.pprint(lda.print_topics(num_words=num_words))
