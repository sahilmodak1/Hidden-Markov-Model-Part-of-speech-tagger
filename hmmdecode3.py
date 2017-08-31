import math
import sys

def hmmcode():
	answer=[]
	path=[]
	if len(path)!=0:
		#print("A: ",a)								
		max=path[dict_key-1][0][2]
		j=0
		for k in path[len(a)-1]:
			if k[2]>max:
				j=path[len(a)-1].index(k)
				max=path[len(a)-1][j][2]


		answer.append(path[len(a)-1][j][1])
		answer.append(path[len(a)-1][j][0])

		i=len(a)-2
		max=-sys.maxsize
		index=-1
		while i>=1:
			max=-sys.maxsize
			for k in path[i]:
				if k[1]==answer[len(answer)-1]:
					if k[2]>max:
						max=k[2]
						index=path[i].index(k)
			#print("i: ",i)
			#print("index: ",index)
			answer.append(path[i][index][0])
			i-=1
	else:
		ans_val=0
		for k in q0:
			if k > ans_val:
				ans_val=k
		answer.append(allTags[q0.index(ans_val)])

	for idx, val in enumerate(reversed(answer)):
		#print(a[idx]+"/"+val)
		output.write((a[idx]+"/"+val+" "))
	output.write("\n")
	#print("\n")

sent=[]	
forMax=dict()		
path=dict()	
file1 = open("hmmmodel.txt","r")

emission_prob=dict()
initial_trans_prob=dict()
trans_prob=dict()
allTags=[]

emission_prob=eval(file1.readline())
initial_trans_prob=eval(file1.readline())
trans_prob=eval(file1.readline())
allTags=eval(file1.readline())

file2=open(sys.argv[1],"r",encoding="utf-8")
file3=open("hmmoutput.txt","w")

for line in file2:
	words=line.split()
	sent=[]
	path=dict()	
	back_tr=dict()
	
	#temp1=[]
	if words[0] in emission_prob:
		temp1=[]
		#path[d]=[]
		for transition in emission_prob[words[0]]:
			temp2=[]
			temp2.extend(["INITIAL_STATE",transition,words[0],math.log(initial_trans_prob[transition]*emission_prob[words[0]][transition])])
			sent.append(temp2)
			if words[0] not in path:
				path[1]=[]
			temp1.append(temp2)
		path[1]=temp1
	
	else:
		temp1=[]
		for transition in initial_trans_prob:
			temp2=[]
			temp2.extend(["INITIAL_STATE",transition,words[0],math.log(initial_trans_prob[transition])])
			sent.append(temp2)
			if words[0] not in path:
				path[1]=[]
			temp1.append(temp2)
		path[1]=temp1

	word_no=0
	#print (len(sent))
	#print (sent)
	#print ("\n")
	#print(sent)
	for word in words[1:]:
		word_no+=1

		back_tr = dict()
		
		while sent!=[]:
			previous=sent[-1]
			del sent[-1]
			mod=previous[1]
			pp=previous[3]
			tf=previous[2]

			if word in emission_prob:
				for transition in emission_prob[word]:
					if transition not in back_tr:
						back_tr[transition]=[]
					#prob=math.log(trans_prob[mod+"-"+transition]*emission_prob[word][transition])+pp
					previous=[mod,math.log(trans_prob[mod+"-"+transition]*emission_prob[word][transition])+pp,word]
					#print(previous)
					back_tr[transition].append(previous)

			else:
				for k in allTags:		
					if k not in back_tr:
						back_tr[k]=[]
					#prob = math.log(trans_prob[mod+"-"+k]) + pp
					previous = [mod, math.log(trans_prob[mod+"-"+k]) + pp,word]
					back_tr[k].append(previous)

		for key1 in back_tr:
			max1=-sys.maxsize
			for key2 in back_tr[key1]:
				if key2[1]>max1:
					max1=key2[1]
					max2=key2

			forPath=[]
			forPath.extend([max2[0],key1,max2[2],max2[1],word_no])
			sent.append(forPath)

			if word_no+1 not in path:
				path[word_no+1]=[]

			path[word_no+1].append(forPath)
		#print ("\n")
		#print (sent)


	"""for k in path:
		print(k," ",path[k])
	print(words)"""

	level=[]
	max1=-sys.maxsize		
	for k in sent:
		if k[3]>max1:
			max1=k[3]
			level=k

	answer=[]
	answer.append(level[1])
	#print("A:",len(answer))

	index=len(words)-1
	while(index>0):
		prev=level[0]
		for k2 in path[index]:
			if k2[1]==prev :
				level=k2
				answer.append(level[1])
		index=index-1

	#print(answer)
	answer=list(reversed(answer))
	#print(answer)
	#print(answer)
	#print("len(w):",len(words))
	#print("len(ans):",len(answer))

	i=0
	for k in words:
		file3.write(k+"/"+answer[i]+" ")
		i+=1
	file3.write("\n")
	#print(answer)

file3.close()
