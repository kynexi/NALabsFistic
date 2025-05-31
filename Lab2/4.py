import numpy as np
import math
import matplotlib.pyplot as plt

data = {}
with open('Lab2\\data\\map.txt') as file:
    for line in file:
        line = line.strip()
        if not line or line.startswith("Coordinate") or line.startswith("-"):
            continue  
        try:
            coord_str, elevation_str = line.split(')')
            coord_str += ')'  
            elevation_str = elevation_str.strip()
            coord_parts = [x.strip() for x in coord_str.strip('()').split(',') if x.strip()]
            coord = tuple(map(int, coord_parts))
            elevation = float(elevation_str) if elevation_str != 'NaN' else float('nan')
            data[coord] = elevation
        except Exception as e:
            print(f"Skipping line due to error: {line} -> {e}")


def inverse_distance_weighting(coord, data, p=2):
    weights = []
    elevations = []
    for c, e in data.items():
        if not math.isnan(e):  # Only consider known points
            d = math.sqrt((coord[0]-c[0])**2 + (coord[1]-c[1])**2)
            if d > 0:  # Avoid division by zero
                weight = 1 / d**p
                weights.append(weight)
                elevations.append(e * weight)
    
    if not weights:
        return None
    return sum(elevations) / sum(weights)

for coord, elevation in data.items():
    if math.isnan(elevation):
        data[coord] = inverse_distance_weighting(coord, data)

for i in data:
    print(i, data[i])



max_x = max(coord[0] for coord in data)
max_y = max(coord[1] for coord in data)

grid = np.zeros((max_y + 1, max_x + 1))  

for (x, y), value in data.items():
    grid[y][x] = value  

# Step 3: Plot heatmap
plt.figure(figsize=(8, 6))
plt.imshow(grid, cmap='terrain', origin='lower')
plt.colorbar(label='Elevation (m)')
plt.title('Interpolated Elevation Map')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(False)
plt.show()