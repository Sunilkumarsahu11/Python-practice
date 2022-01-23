def find_max_binarygap(N) :
  
  binary_equiv = bin(num)[2:]
  #print(binary_equiv)
  start = False
  count = 0
  max = 0
  for i in binary_equiv:
      #print(i)
      if i == '1' and not start:
          #print("1 start found")
          start = True
      elif i == '1' and start :
          #print(" 1 end found")
          if max < count:
              max = count
          count = 0
          #print("Max value",max)
          start = True
      elif i == '0' and start:
          #print(" Gap 0 found")
          count = count +1


  return(max)
