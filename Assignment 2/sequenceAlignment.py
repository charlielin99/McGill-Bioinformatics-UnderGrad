# q1 Initialize alignmentScoreGrid
def initializeAlignmentScoreGrid(seq1, seq2, gap_score):
    alignmentScoreGrid = [[0 for j in range(len(seq2) + 1)] for i in range(len(seq1) + 1)]
    # initialize alignmentScoreGrid for the first column (align seq1 with gaps)
    
    temp = -1  # start filling in x from -1 down to length of x
    for i in range(1, len(seq1) + 1):
        alignmentScoreGrid[i][0] = temp
        temp -= 1
    temp = -1  # reset temp to -1

    for i in range(1, len(seq2) + 1):  # fill in y from -1 down to length of y
        alignmentScoreGrid[0][i] = temp
        temp -= 1
    return alignmentScoreGrid


# Use it to check whether your alignmentScoreGrid is calculated correctly
def printAlignmentGrid(seq1, seq2, alignmentScoreGrid):
    seq1 = "-" + seq1
    seq2 = "-" + seq2

    print(end='\t')

    for j in range(0, len(alignmentScoreGrid[0])):
        print(seq2[j], end='\t')

    print()

    for i in range(0, len(alignmentScoreGrid)):
        print(seq1[i], end='\t')
        for j in range(0, len(alignmentScoreGrid[0])):
            print(alignmentScoreGrid[i][j], end='\t')
        print()


# q2 get sequence alignment values by dynamic programming
def completeAlignmentScoreGrid(seq1, seq2, alignmentScoreGrid,
                               match_score, mismatch_score, gap_score):
    for i in range(1, len(alignmentScoreGrid)):
        for j in range(1, len(alignmentScoreGrid[0])):

            # fill in the algorithm
            # move diagonal
            if seq1[i - 1] == seq2[j - 1]:  # match
                diagonal_move = alignmentScoreGrid[i - 1][j - 1] + match_score
            else:  # mismatch
                diagonal_move = alignmentScoreGrid[i - 1][j - 1] + mismatch_score

            # get score for moving down
            move_down = alignmentScoreGrid[i - 1][j] + gap_score
            # get score for moving right
            move_right = alignmentScoreGrid[i][j - 1] + gap_score

            alignmentScoreGrid[i][j] = max([diagonal_move, move_down, move_right])

    return alignmentScoreGrid


# q3 trace back the optimal alignment by getting the alignmentIndices
def traceback(seq1, seq2, alignmentScoreGrid,
              match_score, gap_score, mismatch_score):
    seq1 = "-" + seq1
    seq2 = "-" + seq2

    seq1_alignment = ""
    seq2_alignment = ""

    i = len(alignmentScoreGrid) - 1
    j = len(alignmentScoreGrid[0]) - 1

    seq2P = j
    seq1P = i

    while i > 0 and j > 0:
        align_score = match_score if seq1[i] == seq2[j] else mismatch_score

        # diagonal
        if alignmentScoreGrid[i][j] == alignmentScoreGrid[i - 1][j - 1] + align_score:

            seq2_alignment += seq2[seq2P]
            seq1_alignment += seq1[seq1P]
            i -= 1
            j -= 1
            seq2P -= 1
            seq1P -= 1

        # up
        elif alignmentScoreGrid[i][j] == alignmentScoreGrid[i - 1][j] + gap_score:

            seq1_alignment += seq1[seq1P]
            seq2_alignment += "-"
            i -= 1
            seq1P -= 1

        # left
        elif alignmentScoreGrid[i][j] == alignmentScoreGrid[i][j - 1] + gap_score:
            seq2_alignment += seq2[seq2P]
            seq1_alignment += "-"
            j -= 1
            seq2P -= 1
        else:
            raise Exception("something is wrong")

    return (seq1_alignment[::-1], seq2_alignment[::-1])


# align main function
def align(seq1, seq2, match_score=2, gap_score=-1, mismatch_score=-2):
    alignmentScoreGrid = initializeAlignmentScoreGrid(seq1, seq2, gap_score)

    alignmentScoreGrid = completeAlignmentScoreGrid(seq1, seq2,
                                                    alignmentScoreGrid,
                                                    match_score,
                                                    mismatch_score, gap_score)

    return (alignmentScoreGrid,
            traceback(seq1, seq2, alignmentScoreGrid,
                      match_score, gap_score, mismatch_score))


# test program for q1-q5
seq1 = "GATTACA"
seq2 = "GCATGCT"

# seq1="GATTACAA"
# seq2="GCAT"

match_score = 2
gap_score = -1
mismatch_score = -2

printAlignmentGrid(seq1, seq2, initializeAlignmentScoreGrid(seq1, seq2, gap_score))

alignmentResults = align(seq1, seq2, match_score, gap_score, mismatch_score)

alignmentScoreGrid = alignmentResults[0]
alignments = alignmentResults[1]

printAlignmentGrid(seq1, seq2, alignmentScoreGrid)
print(alignments[0])
print(alignments[1])
print(alignmentScoreGrid[-1][-1])


# q4 compute pairwise sequence similarity from 8 homologous amino acid sequences
# that code for histone cluster 1 H1 family member a protein for 8 species
seqlist = ["MSETVPPAPAASAAPEKPLAGKKAKKPAKAAAASKKKPAGPSVSELIVQAASSSKERGGVSLAALKKALAAAGYDVEKNNSRIKLGIKSLVSKGTLVQTKGTGASGSFKLNKKASSVETKPGASKVATKTKATGASKKLKKATGASKKSVKTPKKAKKPAATRKSSKNPKKPKTVKPKKVAKSPAKAKAVKPKAAKARVTKPKTAKPKKAAPKKK", # ENST00000244573.4 human
"MSETVPPAPAASAAPEKPLAGKKAKKPAKAAAASKKKPAGPSVSELIVQAASSSKERGGVSLAALKKALAAAGYDVEKNNSRIKLGIKSLVSKGTLVQTKGTGASGSFKLNKKASSVETKPGASKVATKTKATGASKKPKKATGASKKSVKTPKKAKKPAATRKSSKNPKKPKIVKPKKVAKSPAKAKAVKPKAAKAKVTKPKTAKPKKAAPKKK", # Chimp ENSPTRT00000032884.3
"MSETVPTAPAASAAPEKPLAGKKAKKPAKAVVASKKKPAGPSVSELIVQAASSSKERGGVSLAALKKALAVAGYDVEKNNSRIKLGIKSLVSKGTLVQTKGTGASGSFKLNKKAFSVETKPGASKVAAKTKATGASKKLKKATGASKKSVKTPKKAKKPAATRKSSKNPKKPKTLKPKKVAKSPAKAKAVKPKAAKAKVTKPKTAKPKKAAPKKK", # Orangutan ENSPPYT00000018952.1
"MSETAPVAQAASTATEKPAAAKKTKKPAKAAAPRKKPAGPSVSELIVQAVSSSKERSGVSLAALKKSLAAAGYDVEKNNSRIKLGLKSLVNKGTLVQTKGTGAAGSFKLNKKAESKAITTKVSVKAKASGAAKKPKKTAGAAAKKTVKTPKKPKKPAVSKKTSKSPKKPKVVKAKKVAKSPAKAKAVKPKASKAKVTKPKTPAKPKKAAPKKK", # mouse ENSMUST00000055770.3
"MSETAPVPQPASVAPEKPAATKKTRKPAKAAVPRKKPAGPSVSELIVQAVSSSKERSGVSLAALKKSLAAAGYDVEKNNSRIKLGLKSLVNKGTLVQTKGTGAAGSFKLNKKAESKASTTKVTVKAKASGAAKKPKKTAGAAAKKTVKTPKKPKKPAVSKKTSSKSPKKPKVVKAKKVAKSPAKAKAVKPKAAKVKVTKPKTPAKPKKAAPKKK", # rat ENSRNOT00000023054.6 
"MSETAPPASATSTPPEKPAAGKKAKRPAKAAAAAKKKPTGPSVSELIVQAVSSSKERSGVSLAALKKALAAAGYDVEKNNSRIKLGLKSLVSKGTLVQTKGTGASGSFKLNKKAASGEVKANPTKVVKAKVTGTSKKPKKVTAAVKKAVKTPKKAKKPAVTKKSSKSPKKPKVVKPKKVAKSPAKAKAVKPKAAKAKVTKPKTAAKPKKAAPKKK", # Panda ENSAMET00000021358.1
"MSETAPPVPAASTPPEKPSAGRKAKKPAKAVATAKKKPAGPSVSELIVQAVSSSKERSGVSLAALKKALAAAGYDVEKNNSRIKLGLRSLVSKGTLVQTKGTGASGSFKFNKKVASVDSKPSATKVAAKAKVTSSSKKPKKATGAAAGKKGVKTPKNAKKPAATKKSSKSPKKSRVVKPKKIGKSPAKAKAVKPKAAKAKVTKPKTAAKPKKAAPKKK", # Dolphin ENSTTRT00000016728.1
"RSLTSEPSPGKSWDISGAPAKAAKKKTTASKPKKVGPSVGELIVKAVAASKDRSGVSTATLKKALAAGGYDVDKNKACVKTAIKSLVAKGSLVQTKGTGASGSFKMNKKAKKPTKKAAPKAKKPAAAKAKKPATAAKKPKKAAAAKKPTAAKKSPKKAKKAKKPAAAVAKKATKSPKKAAAKSPKKVIKKAPAAKKAPTKKAAKPKAKKAATAAKKKKSPKHK" # Tilapia ENSONIT00000015688.1
]

species = ("human", "chimp", "orangutan", "mouse", "rat", "panda", "dolphin", "tilapia")

def similarityMatrix(seqlist):

    sequenceSimilarity=[[0 for i in range(len(seqlist))] 
                   for j in range(len(seqlist))]

    #YOUR CODE HERE

    # nested for loop to place things inside empty matrix
    for i in range (len(seqlist)):
        for j in range (len(seqlist)):
            temp = align(seqlist[i],seqlist[j])
            # parse out matrix from align
            temp = temp[0]
            # parse out bottom right corner value from matrix
            temp = temp[-1][-1]
            # place value within similitary matrix
            sequenceSimilarity[j][i] = temp

    return sequenceSimilarity

from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
import numpy as np
simmat = similarityMatrix(seqlist)
sequenceSim = np.array(simmat)
dn = hierarchy.dendrogram(hierarchy.linkage(1/sequenceSim, 'single'),
                          labels=species)

plt.show() # remove comment to visualize the species dendrogram cluster


# q5: get consensus sequence based on pairwise similarity
def findConsensusSequence(seqlist_new):

    # recursive code, breaks when sequence list is size one and returns the final consensus sequence
    if len(seqlist_new) == 1:
        return seqlist_new[0]

    aligned_consensus = ""
    #YOUR CODE HERE
    #return "MSETXXPXXXXXAXXAXXXXXEKPXAXXKXKXXXPAKAXXXAXXXKKPXGPSVSELIVQAXSSSKERXGVSLAALKKXLAXAGYDVEKNNSRIKLGXXSLVXKGTLVQTKGTGAXGSFKXNKKXAXXXXXXKXXXXXXKVXXKXKXXXXSXXXKKXKKXTXXXAXKKXVKTPKXXKKPAXXXXTXXXSKXPXKXKXXXXKXKKXXKSPAKAKAVKPKAXKXXXVTKPKTXAKPKKAAPKKK"

    # stores the similitary matrix
    simMatrix = similarityMatrix(seqlist_new)
    # 3 variables to track things, start at value -1
    highScore = -1
    highestXPosition = -1
    highestYPosition = -1

    # use a for loop to iterate through simMatrix
    for i in range (len(seqlist_new)):
        for j in range (len(seqlist_new)):
            # they have to be distinct values so i cannot equal j
            # i only care about new values that have a greater matrix score (indicating more similitary)
            if i!=j and simMatrix[i][j] > highScore:
                # if I enter the if statement, i update the high score and update the x and y columns at which I found them
                highScore = simMatrix[i][j]
                highestXPosition = i
                highestYPosition = j

    # align based on the highest x and y columns
    alignedStrings = align(seqlist_new[highestXPosition], seqlist_new[highestYPosition])
    # extract the two alignment sequence strings
    alignedStrings = alignedStrings[1]

    # empty string
    consensusSequence = ""

    # creating consensus sequence from the two alignment strings
    # append letter if they are the same, append X if different
    for i in range(len(alignedStrings[0])):
        if alignedStrings[0][i] != "-" and alignedStrings[0][i] == alignedStrings[1][i]:
            consensusSequence += alignedStrings[0][i]
        else:
            consensusSequence += "X"

    # cool little function that removes both the x and y column values I used from the sequenceList without messing up Index
    seqlist_new = [v for i, v in enumerate(seqlist_new) if i not in frozenset((highestXPosition, highestYPosition))]

    # append my newly created consensus sequnce
    seqlist_new.append(consensusSequence)

    # call the function recursively with my new seqlist
    return findConsensusSequence(seqlist_new)

seqlist_new = seqlist[0:len(seqlist)-1] # exclude Tilapia sequence
aligned_consensus = findConsensusSequence(seqlist_new)

msa = [] # multiple sequence alignments

print("aligned_consensus")
print(aligned_consensus)

for i in range(0,len(seqlist)-1): # exclude tilapia    
    alignResults = align(seqlist[i], aligned_consensus)[1]    
    msa.append(alignResults[0])

print()
print("Multiple sequence alignment")
for i in range(0, len(msa)):    
    print(species[i])
    print(msa[i])
print()


# q6 (bonus): calculate conservion score in the human sequence 
# relative to the other 6 species

#YOUR CODE HERE

human = msa[0]
# empty list for conservedCounts
conservedCounts = []

# loop through the length of human sequence
for i in range (len(human)):
    # store value of current human sequence index in humanValue
    humanValue = human[i]
    # skip dashes
    if humanValue == "-":
        continue
    # start count value at 0
    count = 0
    for j in range (1, len(msa)):
        # if any other sequence character at the same index is equal to the human value, up the count
        if msa[j][i] == humanValue:
            count += 1
    # append the count to the conservedCounts list outside the j for loop
    conservedCounts.append(count)


human_seq = msa[0].replace('-', '').replace(' ', '')

consPos = 0
for aaPos in range(0,len(human_seq)):
    print(human_seq[aaPos],end='')
    if (aaPos+1) % 50 == 0:        
        print()
        while consPos <= aaPos:
            print(conservedCounts[consPos],end='')
            consPos +=1
        print()
print()        
while consPos <= aaPos:
    print(conservedCounts[consPos],end='')
    consPos +=1