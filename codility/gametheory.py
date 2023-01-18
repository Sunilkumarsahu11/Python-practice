games3 = [1,2] 
n=4
games4 = [[1,2,3,4],[1,3,2,4]]
games = games4
pairs = [(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1)]

def isGamesPlayed(n:int,m:int,games)-> bool:
    for round in games:
    # print(round)
        data = []
        for i, j in pairs:
            isPlayed = True
            #print(i,j)
            
            if i in round[:n // 2] and j in round[:n // 2]:
                # print("Left side ",i,j)
                isPlayed = False
            if i in round[n // 2:] and j in round[n // 2:]:
                # print("Rightt side ",i,j)
                isPlayed=False 
            if isPlayed :
                # print("removing pair ",i,j)
                data.append((i,j))
        
        for d in data:
            pairs.remove(d) 
            
    if len(pairs) > 0:
        return False
    else :
        return True
    

print(isGamesPlayed(2,1,[[1,2]]))
print(isGamesPlayed(4,2,games))