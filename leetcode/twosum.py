from typing import List
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
      # iterate over list starting index with zero
        for i in range(0,len(nums)) :
          # iterate over list again from i+1 location.
            for j in range(i+1,len(nums)) :
              #check if the two numbers are equal to the target
                if nums[i] +nums[j] == target :
                    return [i,j]
                  
                  
 if __name__ == '__main__':
    s = Solution()
    ans = s.twoSum([2,7,4,9],9)
    print(ans)
