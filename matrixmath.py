#referencia https://www.geeksforgeeks.org/c-program-multiply-two-matrices/

def theorem(row, columns):
	matrix = []
	for i in range(row):
		matrix.append([])
		for j in range(columns):
			matrix[-1].append(0.0)
	return matrix

def multM(matrix1,matrix2):	
	
	matrixFinish = theorem(len(matrix1), len(matrix2[0]))
	for i in range(len(matrix1)):
		for j in range(len(matrix2[0])):
			for k in range(len(matrix2)):
				matrixFinish[i][j] += matrix1[i][k] * matrix2[k][j]
	return matrixFinish