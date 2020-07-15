#Code without librarry as numpy, pandas, matlab.
class LinearSpectrum:
    #read text file
    A = []
    with open('/content/tst_20_32.txt') as f:
        for line in f:
            A.append(line.rstrip())
            A = [list(map(int, x)) for x in A]
    n = len(A[0])
    #get vector
    vector = [] #Новая матрица.
    for i in range(len(A)):
        for z in range(1, len(A) - i):
            for j in range(n):
                vector.append(A[i][j] ^ A[i+z][j])
    
    #vectro to matrix
    k = []
    for i in range(len(vector)):
        if i % n == 0: 
            k.append(vector[i:i+n])
    #find weight of lines
    weight = []
    for i in range(len(k)):
        weight.append(sum(k[i]))
    
    #number weight vectors
    z = 0
    x_lim = []
    for j in range(len(k[0])+1):
        for i in range(len(weight)):
            if weight[i] == j:
                z += 1
        x_lim.append(z)
        z = 0
    #time check
    %time
    #save to text
    with open("file.txt", "w") as output:
        for i in range(len(x_lim)):
            output.write(str(i)+'    '+str(x_lim[i])+'\n')
