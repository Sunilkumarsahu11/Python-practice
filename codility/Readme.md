#   Gibonacci series
##  Problem
    write a function which return the nth number from the given gibonacci series gibonacci (n:int, x:int,y:int)

##  Definition 
### A Gibonacci series is defined as :
    F(0) = x where 0 <= x < inf
    F(1) = y where 0 <= y < inf and x > y
    F(n) = F(n-1) - F(n-2) 
    
   Interestingly this series are of fixed numbers and repeat itself after 6n where n >= 0 integer.
   
   For example the first two elements are : [0,1]
   Series : 0 , 1, 1, 0, -1, -1,  0, 1, 1, 0, -1, -1, 0,...
   
   another example  ; [3,8]
   Series : 3, 8, 5, -3, -8, -5,   3, 8, 5,  
 

## solution 
    Please check GibonacciSeries.py for the solution


# Game Theory 

## Problem Statement  
    A game is played between two teams. There are always n number of players and divided into two teams. 
    A given 2D array (mxn) represent the player of each team in each round.
    A row represet one round of the game and each number in the row represent the players permutaions in each team.
    half of the each row represents first team and next half represents the other team
    
 ###  Questions 
     Find out if each players have played at least a match with all other players.
     Examples : (N is no of players)
     games1 = [ [3,1,4,5,6,2], [5,3,2,4,1,6], [5,3,6,4,2,1], [6,5,3,2,1,4], [5,4,1,2,6,3], [4,1,6,2,5,3] ], N = 6
     games2 = [ [1,6,3,4,5,2], [6,4,2,3,1,5], [4,2,1,5,6,3], [4,5,1,6,2,3], [3,2,5,1,6,4], [2,3,6,4,1,5] ], N = 6
     games3 = [1,2], N=2
 
