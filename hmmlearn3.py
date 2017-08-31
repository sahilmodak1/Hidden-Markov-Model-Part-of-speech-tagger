import sys
import math

trans_prob = dict()
words_count = dict()
path = dict()

allTags=[]
allTags_count=[]
allTags_trans=[]
allTags_prob=[]

firstWordTags=[]
firstWordTags_prob=[]




file1=open(sys.argv[1],"r",encoding="utf-8")

for line in file1:
	a=line.split()
	for word in a:
		if word[-2:] not in allTags:
			allTags.append(word[-2:])
			allTags_count.append(0)
		if word is a[0] and word[-2:] not in firstWordTags:
			firstWordTags.append(word[-2:])
			firstWordTags_prob.append(0)
		if word not in words_count:
			words_count[word]=1
		elif word in words_count:
			words_count[word]+=1

file1.close()

file1=open(sys.argv[1],"r",encoding="utf-8")
for line in file1:
	a=line.split()[0]															#firstWordTags: [VB,NN]
	firstWordTags_prob[firstWordTags.index(a[-2:])]+=1					  		#firstWordTags_prob: [2,8]
file1.close()
	


#Smoothing for Layer 1
firstwordtags_prob1=[]
for k in allTags:													#allTags: [VB,NN,IN,DT]
	firstwordtags_prob1.append(0)									#firstwordtags_prob1: [0,0,0,0]

for k in allTags:
	if k in firstWordTags:
		firstwordtags_prob1[allTags.index(k)]=firstWordTags_prob[firstWordTags.index(k)]+1			#firstwordtags_prob1: [3,9,1,1]
	else:
		firstwordtags_prob1[allTags.index(k)]=1

firstWordTags=allTags
firstWordTags_prob=firstwordtags_prob1

#print("firstwordtags: ",firstWordTags)
#print("firstwordtags_prob: ",firstWordTags_prob)
#Smoothing for Layer 1

for word1 in allTags:
	for word2 in allTags:
		allTags_trans.append(word1+"-"+word2)					#allTags_trans: [VB-VB,VB-NN,VB-IN,VB-DT,NN-VB,NN-NN,NN-IN,NN-DT,IN-VB,IN-NN,IN-IN,IN,DT,.......,DT-DT]
		allTags_prob.append(0);									#allTags_prob: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

#print(allTags)
#print(allTags_trans)

file1=open(sys.argv[1],"r",encoding="utf-8")
for line in file1:
	a=line.split()
	i=0
	while(i<len(a)-1):														#NN-VB: count(NN-->VB)/count(NN-->anything)
		allTags_prob[allTags_trans.index(a[i][-2:]+"-"+a[i+1][-2:])]+=1		#allTags_prob: count(tag1-->tag2)	
		allTags_count[allTags.index(a[i][-2:])]+=1							#allTags_count: count(tag1)		except last column
		i+=1
file1.close()

#print("allTags_trans",allTags_trans)
#print("\n")
#print("allTags_prob",allTags_prob)
#print("\n")
#print("allTags_count",allTags_count)
#print("\n")

#use allTags_count1 for emission
allTags_count1=[]
for k in allTags_count:
	allTags_count1.append(k)		

#Smoothing for all other Layers
for idx, val in enumerate(allTags_prob):
	allTags_prob[idx]+=1

for idx, val in enumerate(allTags_count):
	allTags_count[idx]+=len(allTags)

#print("alltags_prob: ",allTags_prob)
#print("alltags_count: ",allTags_count)

#Smoothing for all other Layers
initial_trans_prob = dict()
k=0
for j in firstWordTags:
	initial_trans_prob[j]=(firstWordTags_prob[k]/sum(firstWordTags_prob))
	k+=1

k=0
for j in allTags_trans:
	trans_prob[j]=allTags_prob[k]
	#print("T: ",trans_prob[j])
	k+=1

#print("TAGS: ",allTags)
for key in trans_prob:
	if key[:-3] != "INITIAL_STATE":
		#print("K: ",key)
		#print("1: ",trans_prob[key])
		#print("2: ",allTags_count[allTags.index(key[:-3])])
		#trans_prob[key]=math.log(trans_prob[key]/allTags_count[allTags.index(key[:-3])]*1.0)
		trans_prob[key]=(trans_prob[key]/allTags_count[allTags.index(key[:-3])]*1.0)



file1=open(sys.argv[1],"r",encoding="utf-8")
#file1=open("catalan_corpus_train_tagged.txt","r")
for line in file1:
	a=line.split()
	allTags_count1[allTags.index(a[len(a)-1][-2:])]+=1
file1.close()

#print("allTags: ",allTags)
#print("allTags_count1: ",allTags_count1)
#print(words_count)
emission_prob=dict()
temp=dict()
file2=open(sys.argv[1],"r",encoding="utf-8")

for word1 in words_count:
	#row.append(math.log(words_count[word1+"/"+word2]/allTags_count1[allTags.index(word2)]))
	if word1[:-3] not in emission_prob:
		temp[word1[-2:]]=words_count[word1]/allTags_count1[allTags.index(word1[-2:])]
		emission_prob[word1[:-3]]=temp
		temp=dict()
	else:
		temp=emission_prob[word1[:-3]]
		temp[word1[-2:]]=words_count[word1]/allTags_count1[allTags.index(word1[-2:])]
		emission_prob[word1[:-3]]=temp
		temp=dict()

	#row.append((words_count[word1+"/"+word2]/allTags_count1[allTags.index(word2)]))

#print(emission_prob)
file2.close()

file_4=open("hmmmodel.txt","w")
file_4.write(str(emission_prob)+"\n")
file_4.write(str(initial_trans_prob)+"\n")
file_4.write(str(trans_prob)+"\n")
file_4.write(str(allTags)+"\n")
filr4.write(str(allTags_trans))
file_4.close()

