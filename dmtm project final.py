#CS583 DATA MINING AND TEXT MINING
#authors-Namaswi Chandarana(nchand22@uic.edu),Vanisre Jaiswal(vjaisw2@uic.edu)
# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
print("Import")
# Importing the dataset
dataset = pd.read_csv('data_2_train.csv')
#dataset=dataset.drop(dataset.index[2053])
dataset.head()

total_rows = len(dataset.index)
cols = list(dataset.columns.values)

# Cleaning the texts
import re
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
dataset[' text']=dataset[' text'].replace("comma","",regex=True)
dataset[' text']=dataset[' text'].replace("\[]","",regex=True)

corpus = []
for i in range(0, total_rows):
    review = re.sub('[^a-zA-Z]', ' ', dataset[' text'][i])
    review = review.lower()
    review = review.split()
    #ps = PorterStemmer()
    #review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    review = ' '.join(review)
    corpus.append(review)


#dependency parsing using spacey
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()
dep_par=[]
for i in range(0, total_rows):
 doc = nlp(unicode(corpus[i], "utf-8"))
 dep_par.append(doc)

 
aspect_term=[]
for i in range(0, total_rows):
    review = re.sub('[^a-zA-Z]', ' ', dataset[' aspect_term'][i])
    review = review.lower()
    review = review.split()
    #ps = PorterStemmer()
    #review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    review = ' '.join(review)
    aspect_term.append(review)

dataset['loc_start']=dataset[' term_location'].replace("--[0-9]+","",regex=True)
dataset['end']=dataset[' term_location'].replace("[0-9]+--","",regex=True)
loc_start=[]
loc_start=dataset['loc_start'].tolist()
loc_end=[]
loc_end=dataset['end'].tolist()


from spacy import displacy
displacy.render(dep_par[4],style='dep')

def check_similarity(text,aspect):
    for word in aspect.split():
     #print word,text
     if text==word:
        #print("True")
        return True
    return False

from spacy.symbols import nsubj, VERB,ADJ,amod,NOUN,acomp,dep,advmod,ccomp,pobj,prep,dobj,ADV,neg,attr

def get_adj(i,start_loc,end_loc):
    #i=4
    dep_par1=dep_par[i]
    aspect_term1=aspect_term[i]
    #start_loc=int(start_loc)-2
    #end_loc=int(end_loc)+2
    #dep_par1=dep_par[12]
    #aspect_term1=aspect_term[12]
    start_loc=int(loc_start[i])-2
    end_loc=int(loc_end[i])+2
    adj=[]
    temp=[]
    temp1=[]
    temp2=[]
    temp3=[]
    temp4=[]
    
    for possible_subject in dep_par1:
        temp.append(possible_subject)
        if possible_subject.dep == advmod:
            temp1.append(possible_subject.text)
            if possible_subject.head.pos==VERB or possible_subject.head.pos==NOUN:
                temp2.append(possible_subject.head.text)
                if check_similarity(possible_subject.head.text,aspect_term1) and possible_subject.head.idx>=start_loc and possible_subject.head.idx<=end_loc:
                    temp3.append(True)
                    adj.append(possible_subject.text)
                    
    for possible_subject in dep_par1:
        temp.append(possible_subject.head.text)
        if possible_subject.pos == NOUN and check_similarity(str(possible_subject.head.text),aspect_term1) and possible_subject.dep_ == 'compound':
          temp1.append(possible_subject.text)
          temp3.append(check_similarity(str(possible_subject.text),aspect_term1))
          if check_similarity(str(possible_subject.text),aspect_term1):
                 for children in possible_subject.head.rights:
                     temp2.append(children.text)
                     if children.pos==NOUN:
                         adj.append(children.text)
    
    for possible_subject in dep_par1:
       if check_similarity(str(possible_subject.text),aspect_term1) and possible_subject.dep == dobj:
           adj.append(possible_subject.head.text)
           for children in possible_subject.head.lefts:
               if children.pos==ADV:
                adj.append(children.text)
           
                          
    count=0
    for possible_subject in dep_par1:
        if possible_subject.dep == nsubj and check_similarity(str(possible_subject.text),aspect_term1):
             temp.append(possible_subject.text)
             for right_children in possible_subject.head.rights:
                    temp2.append(right_children.text)
                    for right_children1 in right_children.lefts:
                        
                         temp3.append(right_children1.text)
                        
                         if right_children1.dep==amod: 
                          adj.append(right_children1.text)
                        
                    
    
    for possible_subject in dep_par1:
        if possible_subject.pos==NOUN :
            count=count+1
    if count==1:
        for possible_subject in dep_par1:
            if possible_subject.pos==ADV or possible_subject.pos==ADJ:
                adj.append(possible_subject.text)
        
    for possible_subject in dep_par1:
        if possible_subject.dep == nsubj and check_similarity(str(possible_subject.text),aspect_term1):
                temp.append(possible_subject.text)
            
                for left_children in possible_subject.head.rights:
                    temp2.append(left_children.text)
                    if left_children.dep==attr:
                        adj.append(left_children.text)
                        
    for possible_subject in dep_par1:
        if possible_subject.dep == attr and check_similarity(str(possible_subject.text),aspect_term1):
                temp.append(possible_subject.text)
            
                for left_children in possible_subject.head.lefts:
                    temp2.append(left_children.text)
                    if left_children.dep==nsubj:
                        adj.append(left_children.text)
    
    for possible_subject in dep_par1:
        if possible_subject.dep == pobj and check_similarity(str(possible_subject.text),aspect_term1):
            temp.append(possible_subject.text)
            if possible_subject.head.dep == prep:
                temp1.append(possible_subject.head.text)
                count=0
                for left_children in possible_subject.head.ancestors:
                    count=count+1
                    if count!=2:
                        temp2.append(left_children.text)
                        if left_children.pos==ADJ:
                            adj.append(left_children.text)
                            
                    else:
                        break
                
        
    
    for possible_subject in dep_par1:
        temp.append(possible_subject.text)
        adj_caught=-1
        adj_caught_loc=-1
        if possible_subject.dep == acomp or possible_subject.dep == ccomp:
            #temp1.append(True)
            if possible_subject.head.pos == VERB:
                #temp2.append(True)
                
                #temp3.append(possible_subject.head.text)
                for left_children in possible_subject.head.lefts:
                    if check_similarity(str(left_children.text),aspect_term1) and left_children.idx>=start_loc and left_children.idx<=end_loc:
                     adj_caught=possible_subject.text
                     adj_caught_loc=possible_subject.idx
                     
                     temp4.append(adj_caught_loc)
                     adj.append(possible_subject.text)
            if adj_caught != -1:
             for possible_subject1 in dep_par1:
            
              if possible_subject1.dep == advmod:
               temp1.append(possible_subject.text)
               temp2.append(possible_subject.head.text)
            
               if str(adj_caught)==str(possible_subject1.head.text) :#and possible_subject.head.idx==adj_caught_loc :
                temp3.append(True)
                adj.append(possible_subject1.text)
            #temp4.append(possible_subject.text)
                       
                
    
    for possible_subject in dep_par1:
        temp.append(possible_subject)
        if possible_subject.dep_ == 'compound' :
            temp1.append(True)
            if possible_subject.head.pos==NOUN or possible_subject.head.pos==ADJ:
                temp2.append(True)
                if check_similarity(possible_subject.head.text,aspect_term1) and possible_subject.head.idx>=start_loc and possible_subject.head.idx<=end_loc:
                    temp3.append(True)
                    adj.append(possible_subject.text)
                    
    for possible_subject in dep_par1:
        temp.append(possible_subject)
        if possible_subject.dep == amod:
            temp1.append(True)
            if possible_subject.head.pos==NOUN or possible_subject.head.pos==ADJ:
                temp2.append(True)
                if check_similarity(possible_subject.head.text,aspect_term1) and possible_subject.head.idx>=start_loc and possible_subject.head.idx<=end_loc:
                    temp3.append(True)
                    adj.append(possible_subject.text)
    
   
    for possible_adj in dep_par1:
        
        if possible_adj.pos == ADJ:
            
            for possible_subject in possible_adj.children:
                #print possible_subject.text,possible_adj.children
                if possible_subject.text == aspect_term1:                  
                    adj.append(possible_adj)
                    break
    if len(adj)==0:
        for possible_subject in dep_par1:
            if check_similarity(possible_subject.text,aspect_term1):
                 temp1.append(True)
#                 for left_children in possible_subject.head.lefts:
#                     temp2.append(left_children.text)
#                     adj.append(left_children.text)
                 for left_children in possible_subject.head.rights:
                     temp2.append(left_children.text)
                     adj.append(left_children.text)
    if len(adj)==0:
        for possible_subject in dep_par1:
            if check_similarity(possible_subject.text,aspect_term1):
                 temp1.append(True)
                 for left_children in possible_subject.head.lefts:
                     temp2.append(left_children.text)
                     adj.append(left_children.text)
#                 for left_children in possible_subject.head.rights:
#                     temp2.append(left_children.text)
#                     adj.append(left_children.text)
    if len(adj)==0:
       for possible_adj in dep_par1:
        
        if possible_adj.pos == ADJ or possible_adj.pos == ADV:
                                         
                    adj.append(possible_adj.text)
                    
        
        
    return set(adj)
        
        
    

adj = []
for i in range(0, total_rows):
 #print dep_par[i]
 temp=get_adj(i,loc_start[i],loc_end[i])
 adj.append(temp)
 
#word_tokenize accepts a string as an input, not a file.
stop_words = set(stopwords.words('english'))
#stop_words =['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']
adj_stop=[]
for i in range(0, total_rows):
    adj_stop_temp=[]
    for r in adj[i]:
     if not r in stop_words:
        adj_stop_temp.append(str(r))
    adj_stop.append(' '.join(word for word in adj_stop_temp))
    
## Creating the Bag of Words model



from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
X=cv.fit_transform(adj_stop).toarray()

lex_file_laptop=pd.read_table("Amazon-laptop-electronics-reviews/Amazon-laptops-electronics-reviews-unigrams.txt",header=None)########## Enter transaction file here 
lex_file_laptop=lex_file_laptop.iloc[0:, 0].str.split(',', expand=True)
lex_file_laptop=lex_file_laptop.iloc[0:, 0:2]
lex_file_laptop.replace(to_replace="FIRST",value="",regex=True,inplace=True)
lex_file_laptop.replace(to_replace="_NEG",value="",regex=True,inplace=True)
lex_file_laptop=lex_file_laptop.set_index(0).to_dict()[1]
#
lex_file_res=pd.read_table("Yelp-restaurant-reviews/Yelp-restaurant-reviews-unigrams.txt",header=None)########## Enter transaction file here 
lex_file_res=lex_file_res.iloc[0:, 0].str.split(',', expand=True)
lex_file_res=lex_file_res.iloc[0:, 0:2]
lex_file_res.replace(to_replace="FIRST",value="",regex=True,inplace=True)
lex_file_res.replace(to_replace="_NEG",value="",regex=True,inplace=True)
lex_file_res=lex_file_res.set_index(0).to_dict()[1]

lex_file_bing_negative=pd.read_table("negative-words.txt",header=None)
lex_file_bing_negative[1]=-1
lex_file_bing_negative=lex_file_bing_negative.set_index(0).to_dict()[1]

lex_file_bing_positive=pd.read_table("positive-words.txt",header=None)
lex_file_bing_positive[1]=1
lex_file_bing_positive=lex_file_bing_positive.set_index(0).to_dict()[1]

def listsum(numList):
    theSum = 0
    for i in numList:
        theSum = theSum + float(i)
    return theSum

def get_lex_score(word):
    #word='horrible'
    lex_scores=[]
    #########Laptop
    if(lex_file_laptop.get(word)!=None):
        lex_scores.append(lex_file_laptop.get(word))
    
    #########Res
    if(lex_file_res.get(word)!=None):
        lex_scores.append(lex_file_res.get(word)-0.5)
        
    ##########Bing LIU
    if(lex_file_bing_negative.get(word)!=None):
        lex_scores.append(lex_file_bing_negative.get(word))
    if(lex_file_bing_positive.get(word)!=None):
        lex_scores.append((lex_file_bing_positive.get(word)))
    ###
    if len(lex_scores)==0:
        lex=0
    else:
        
        lex=listsum(lex_scores)/len(lex_scores)
        
    
    return lex
    


X=X.astype(float)
temp1=[]
temp2=[]
temp=[]
temp3=[]
cv_list=cv.get_feature_names()  
Xbackup=X  
for rowNum in range(np.shape(X)[0]):
    row= X[rowNum]
#    temp.append(row)
    for i in range(row.size): 
        temp1.append(row[i])
        if(row[i]!=0):
                #if(lex_file_laptop.get(cv_list[i])!=None):
                #temp2.append(float(lex_file_laptop.get(cv_list[i])))
                    row[i]=float(get_lex_score(cv_list[i]))
                   #print(float(get_lex_score(cv_list[467])))
                   #print(float(get_lex_score('exceptional')))
#                else:
#                    row[i]=0
#                    temp3.append(row[i])
    
    X[rowNum]=row
temp=[]
pd.DataFrame(X).fillna(0,inplace=True)
X=Xbackup
####################################################
for column in range(np.shape(X.T)[0]):
    #print (column)
    if(sum(X.T[column])==0):
        #print(sum(X.T[column]))
        temp.append(column)
    
X=np.delete(X, temp,axis=1)
    
    

####################################################

y=dataset[' class']

from sklearn.linear_model import LogisticRegression
class_weight = {-1: 1.,
                0: 2.,
                1: 0.9}
classifier = LogisticRegression(random_state = 0,class_weight=class_weight)



from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score

# Applying 10-Fold Cross Validation
from sklearn.model_selection import cross_val_predict,cross_val_score
accuracies = cross_val_predict(estimator = classifier, X = X, y = dataset[' class'], cv = 10, n_jobs=1)
print("10-Fold Cross Validation done")

accuracies.mean()
#accuracies.std()

accScore = accuracy_score(dataset[' class'],accuracies)
labels = [-1,0,1]
precision = precision_score(dataset[' class'], accuracies, average=None,labels=labels)
recall = recall_score(dataset[' class'],accuracies,average=None,labels=labels)
f1score = f1_score(dataset[' class'],accuracies,average=None,labels=labels)



