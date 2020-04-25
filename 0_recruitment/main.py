with open("medium.txt") as file:
    input_data = file.readlines()

array_int = list()

for i in range(len(input_data)):
    counter = 0
    array_int.append([0]*(i+1))
    for j in range(len(input_data[i])):
        try:
            tmp = int(input_data[i][j])
            array_int[i][counter] = tmp
            counter+=1
        except:
            pass

def findPath(arr):
    memo = [None] * len(arr)
    tmp_str = len(arr) * ['']
    n = len(arr) - 1
    
    for i in range(len(arr[n])):
        memo[i] = arr[n][i]
        tmp_str[i] += str(arr[n][i])

    for i in range(len(arr)-2,-1,-1):
        for j in range(len(arr[i])):
            if memo[j]>=memo[j+1]:
                tmp_str[j] = str(arr[i][j]) + tmp_str[j+1]
                memo[j] = arr[i][j] + memo[j+1]
            else:
                memo[j] = arr[i][j] + memo[j]
                tmp_str[j] = str(arr[i][j]) + tmp_str[j]
            
    return memo[0], tmp_str[0]

a, c = findPath(array_int)
print("sum : " + str(a) + " path : " + c)
