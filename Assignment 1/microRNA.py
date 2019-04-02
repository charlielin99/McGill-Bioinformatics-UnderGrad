# complete the program by writing your own code here

mRNA = input("Enter a mRNA sequence: ")
miRNA = input("Enter a microRNA sequence: ")
def rnaMatch (a,b) : # matching function for mRNA
	index = 0
	for c in a :
		scanNuc = b [index]
		if scanNuc == "G" and c != "C" : # looking for Watson-Crick base pairing
			return False # seed match not found
		if scanNuc == "C" and c != "G" : 
			return False
		if scanNuc == "A" and c != "U" : 
			return False
		if scanNuc == "U" and c != "A" :
			return False
		index = index + 1 # continue to next nucleotide
	return True # seed match found
siteNum = 0 # extract index
seed = miRNA[1:7] # create seed using nucleotides 2-7 of miRNA
seed = seed[::-1] # reverse string
for x in range (0,len(mRNA)-6) :
	if (rnaMatch (seed,mRNA[x:x+6]) ) : # looking at 6 consecutive base pairs in mRNA
		siteNum = siteNum + 1 # update index
		print("Match found at nucleotide",x)
print("The mRNA has", siteNum, "target site(s)")