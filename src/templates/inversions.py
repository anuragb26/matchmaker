arr = [1,20,6,4,5]



def countInversions(arr):
	print arr
	return modifiedMergeSort(arr[:])

def modifiedMergeSort(arr):
	invCount = 0
	if(len(arr) > 1):
		mid = len(arr)//2
		left = arr[0:mid]
		right = arr[mid:]
		invCount+=modifiedMergeSort(left)
		invCount+= modifiedMergeSort(right)
		invCount+=merge(arr,left,right)
	return invCount
	
	
def merge(arr,left,right):
	i=0
	j=0
	k=0
	invCount =0
	while(i < len(left) and j < len(right)):
		if(left[i] < right[j]):
			arr[k]= left[i]
			i+=1
		elif(left[i]>right[j]):
			invCount+=1
			arr[k]=right[j]
		k+=1
	while(i<len(left)):
		arr[k]=left[i]
		k+=1
		i+=1
	while(j<len(right)):
		arr[k]=right[j]
		j+=1
		k+=1
	return invCount

print arr
print countInversions(arr)


#print countInversions(arr)