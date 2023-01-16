def solution(n:int,x:int,y:int):
    res = [-1]*6
    n = n%6 
    
    res[0]=x
    res[1]=y
    for i in range(2,6):
        res[i]=res[i-1]-res[i-2]

    return res[n]


solution(2,0,1)