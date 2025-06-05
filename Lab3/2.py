import numpy as np

# Load the connectivity matrix from file
with open('Lab3\\matrix.txt', 'r') as file:
    matrix = [line.strip().split() for line in file]

# Extract node names
names = [name.strip(" '[],") for name in matrix[0][1:] if len(name) > 3]

# Convert string values into float numbers for the adjacency matrix
numbers = np.array([
    [float(x.replace(',', '').replace('[','').replace(']','')) for x in row[1:]]
    for row in matrix[1:]
])

# Compute eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(numbers)

# Identify the dominant eigenvalue and corresponding eigenvector
influential_index = np.argmax(np.abs(eigenvalues)) 
influential_eigenvalue = eigenvalues[influential_index]
influential_eigenvector = eigenvectors[:, influential_index]

# Find the most influential person (largest absolute value in eigenvector)
most_influential_person_index = np.argmax(np.abs(influential_eigenvector))
print("The most influential person is", names[most_influential_person_index],
      "with centrality score =", influential_eigenvector[most_influential_person_index])
print("Corresponding eigenvector:")
print(influential_eigenvector)
print()

# Normalize and rank centrality scores
norm_scores = np.abs(influential_eigenvector)
norm_scores /= norm_scores.sum()

ranked = sorted(zip(names, norm_scores), key=lambda x: -x[1])
print("Influence ranking (normalized):")
for name, score in ranked:
    print(f"{name}: {score:.3f}")
print()

# Print all eigenvalues and eigenvectors
for i, (eigval, eigvec) in enumerate(zip(eigenvalues, eigenvectors.T), start=1):
    print(f"Eigenvalue λ{i}: {eigval}")
    print(f"Eigenvector v{i}:")
    print(eigvec)
    print()

# Sort eigenvalues and eigenvectors for further inspection
sort_indices = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[sort_indices]
eigenvectors = eigenvectors[:, sort_indices]

print("Sorted eigenvalues (descending):")
for eigenvalue in eigenvalues:
    print(eigenvalue)
print()

print("Sorted eigenvectors (corresponding to sorted eigenvalues):")
for eigenvector in eigenvectors.T:
    print(eigenvector)
