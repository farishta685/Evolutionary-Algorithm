import random

#Insert Mutation
def insert(inputList):
    #Turning into a list because string is immutable
    s = inputList
    swapNum1 = random.randint(0, 8)
    swapNum2 = random.randint(0, 8)
    
    #check for swapping same value
    while swapNum2 == swapNum1:
        swapNum2 = random.randint(0, 8)
        
    if min(swapNum1,swapNum2) == swapNum1:
        s.insert(swapNum1+1, s.pop(swapNum2))
    else:
        s.insert(swapNum2+1, s.pop(swapNum1))
    
    return s

#Swap Mutation
def swap(inputList):
    #Turning into a list because string is immutable
    s = inputList
    
    swapNum1 = random.randint(0, 8)
    swapNum2 = random.randint(0, 8)
    
    #check for swapping same value
    while swapNum2 == swapNum1:
        swapNum2 = random.randint(0, 8)
    
    numStorage = s[swapNum1]   
    
    s[swapNum1] = s[swapNum2]
    s[swapNum2] = numStorage
    return s

#Inversion Mutation
def inversion(inputList):
    s = inputList
    
    swapNum1 = random.randint(0, 8)
    swapNum2 = random.randint(0, 8)
    stop = 0
    start = 0
    
    #check for swapping same value
    while swapNum2 == swapNum1:
        swapNum2 = random.randint(0, 8)
    
    #checking for minimum value to swap
    if min(swapNum1,swapNum2) == swapNum1:
        start = swapNum1
        stop = swapNum2
    else:
        start = swapNum2
        stop = swapNum1
    
    size = stop + start
    for i in range(start, (size + 1) // 2 ):
        j = size - i
        s[i], s[j] = s[j], s[i]
        
    return s

def scramble(inputList):
    s = inputList
    
    swapNum1 = random.randint(0, 8)
    swapNum2 = random.randint(0, 8)
    stop = 0
    start = 0
    
    #check for swapping same value
    while swapNum2 == swapNum1:
        swapNum2 = random.randint(0, 8)
    
    #checking for minimum value to swap
    if min(swapNum1,swapNum2) == swapNum1:
        start = swapNum1
        stop = swapNum2
    else:
        start = swapNum2
        stop = swapNum1
    
    size = stop + start
    for i in range(stop, start, -1):
     
        # Pick a random index from 0 to i
        j = random.randint(start, i)
   
        # Swap arr[i] with the element at random index
        s[i], s[j] = s[j], s[i]
        
    return s


def mutation(inputList, mutationType):
    if mutationType == "Swap":
        return swap(inputList)
    elif mutationType == "Insert":
        return insert(inputList)
    elif mutationType == "Inversion":
        return inversion(inputList)
    elif mutationType == "Scramble":
        return scramble(inputList)
