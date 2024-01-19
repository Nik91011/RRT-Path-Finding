import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import argparse
import sys

map_img = cv.imread("maps/" + sys.argv[1] + ".png")

max_x = map_img.shape[1]
max_y = map_img.shape[0]

startx = int(sys.argv[2])
starty = int(sys.argv[3])

goalx = int(sys.argv[4])
goaly = int(sys.argv[5])

starting_point = (startx, starty, 0)
goal_point = (goalx, goaly)


print("Max area is (X, Y) =", (max_x, max_y))

example_x = 513
example_y = 403

class RandomTree():
    
    def __init__(self, starting_point) -> None:
        
        self.start_x = starting_point[0]
        self.start_y = starting_point[1]
        
        self.tree = {starting_point[2] : []}
        
        self.location_map = {starting_point[2] : (self.start_x, self.start_y)}
        
    def addtotree(self, point):
        
        point_x = point[0]
        point_y = point[1]
        point_id = point[2]
        
        self.tree[point_id] = []
        
        self.location_map[point_id] = (point_x, point_y)
        
    def addalink(self, id_1, id_2, dist):      
        

        assert id_1 in self.tree and id_2 in self.tree, "Assertion Failed so printing the tree and then location map" + "\n" + str(self.tree) + "\n" + str(self.location_map)
        
        self.tree[id_1].append((id_2, dist))

        

def draw_path(map_img, new_node, goal_node):
    
    print("Finding the optimal path")
    
    map_img = cv.line(map_img, (new_node[0], new_node[1]), (goal_node[0], goal_node[1]), (255, 0, 0), 2)
    
    new_node_id = new_node[2]
    
    while new_node_id != 0:
        
        parent_node = random_tree.tree[new_node_id]    

        parent_node_id = parent_node[0][0]
        parent_node_dist = parent_node[0][1]
        
        
        map_img = cv.line(map_img, (random_tree.location_map[new_node_id][0], random_tree.location_map[new_node_id][1]), (random_tree.location_map[parent_node_id][0], random_tree.location_map[parent_node_id][1]), (255, 0, 0), 2)
    
        new_node_id = parent_node_id
        
    return map_img

        
print("Initializing the tree and location map")

random_tree = RandomTree(starting_point)


obstacle_map = []
print("Building the obstacle map")

for i in range(map_img.shape[0]):
    for j in range(map_img.shape[1]):
        
        if map_img[j][i][0] == 0:
            obstacle_map.append([i, j])

map_img = cv.circle(map_img, (starting_point[0], starting_point[1]), 5, (0, 0, 255), 5)
map_img = cv.circle(map_img, (goal_point[0], goal_point[1]), 5, (0, 0, 255), 5)
    

test_tree = False

if test_tree == True:
    testing_point = (300, 400, 1)
    random_tree.addtotree(testing_point)
    random_tree.addalink(starting_point[2], testing_point[2])
    
    map_img = cv.circle(map_img, (testing_point[0], testing_point[1]), 2, (255, 0, 0), 5)

    print("After testing, tree looks like", random_tree.tree)
    print("After testing, location map looks like", random_tree.location_map)
    
    randx = np.random.randint(low = 0, high = max_x)
    randy = np.random.randint(low = 0, high = max_y)
    
    count = 2
    
    new_rand_point = (randx, randy, count)
    
    print("Random generator", randx, randy)
    
    map_img = cv.circle(map_img, (new_rand_point[0], new_rand_point[1]), 2, (255, 255, 0), 5)
    
    
    
    print("New Random point is", new_rand_point)
    
    min_temp_dist = float('inf')
    min_id = -1
    
    for k, v in random_tree.tree.items():
        

        print(random_tree.location_map[k][0])
        print(random_tree.location_map[k][1])

        x2_m_x1 = np.power(new_rand_point[0] - random_tree.location_map[k][0], 2)
        y2_m_y1 = np.power(new_rand_point[1] - random_tree.location_map[k][1], 2)
        temp_dist = np.sqrt(x2_m_x1 + y2_m_y1)
        
        print("Distance is", temp_dist)
        
        if temp_dist < min_temp_dist:
            min_temp_dist = temp_dist
            min_id = k
    
    print("ID of the nearest node is", min_id)
    print("Distance between nearest node and random point is", min_temp_dist)
    
    active_node_id = min_id
    
    active_node = (int(random_tree.location_map[active_node_id][0]), int(random_tree.location_map[active_node_id][1]), active_node_id)
    
 
    new_node_x = (new_rand_point[0] + random_tree.location_map[active_node_id][0]) / 2
    new_node_y = (new_rand_point[1] + random_tree.location_map[active_node_id][1]) / 2
    

    
    new_node = (int(new_node_x), int(new_node_y), count)
    print("New node location is", new_node)
    
    map_img = cv.circle(map_img, (int(new_node_x), int(new_node_y)), 1, (255, 0, 0), 3)
        
    x1 = new_node[0]
    y1 = new_node[1]
    
    x2 = active_node[0]
    y2 = active_node[1]
    
    slope = (y2 - y1) / (x2 - x1)
    
    y_intercept = y2 - (slope * x2)
    
    print("Slope and Y-Intercept are", slope, y_intercept)
    
    low_lim = 0.995
    high_lim = 1.015
    
    for points in obstacle_map:
        
        x_point = points[0]
        y_point = points[1]
        
        # Condition of limit check
        if (x_point > max(active_node[0], new_node[0]) or x_point < min(active_node[0], new_node[0])) or (y_point > max(active_node[1], new_node[1]) or y_point < min(active_node[1], new_node[1])):
            print("Obstacle is outside the two nodes so ignoring it")
            continue
        
        
    
        if ((slope * x_point) + y_intercept) / y_point > low_lim and ((slope * x_point) + y_intercept) / y_point < high_lim:
            
            print("There is obstacle in the middle")
            print("Value is", ((slope * x_point) + y_intercept) / y_point)
            # Line between obstacle and new node
            map_img = cv.line(map_img, (x_point, y_point), (new_node[0], new_node[1]), (0, 0, 255), 2)
            # Line between active node and new node
            map_img = cv.line(map_img, (active_node[0], active_node[1]), (new_node[0], new_node[1]), (255, 0, 255), 2)
            
            
        
    
    
    plt.imshow(map_img)
    plt.show()
    

path_found = False

count = 1

dist_threshold = 200

print("Building the Rapidly-exploring Random Tree")

while not path_found:
    
    randx = np.random.randint(low = 0, high = max_x)
    randy = np.random.randint(low = 0, high = max_y)
    
    

    if map_img[randy][randx][0] == 0:
        
        # That means black region
        continue
    
    # Random poinnt generate din the white region
    
    new_rand_point = (randx, randy, count)
    count += 1
    
    min_temp_dist = float('inf')
    
    # Find the nearest node from the new point
    
    for k, v in random_tree.tree.items():

        x2_m_x1 = np.power(new_rand_point[0] - random_tree.location_map[k][0], 2)
        y2_m_y1 = np.power(new_rand_point[1] - random_tree.location_map[k][1], 2)
        temp_dist = np.sqrt(x2_m_x1 + y2_m_y1)
        
        if temp_dist < min_temp_dist:
            min_temp_dist = temp_dist
            min_id = k
            
    if min_temp_dist > dist_threshold:

        continue
    
            
    active_node_id = min_id

    active_node = (int(random_tree.location_map[active_node_id][0]), int(random_tree.location_map[active_node_id][1]), active_node_id)
    
    
    new_node_x = (new_rand_point[0] + random_tree.location_map[active_node_id][0]) / 2
    new_node_y = (new_rand_point[1] + random_tree.location_map[active_node_id][1]) / 2
    
    new_node = (int(new_node_x), int(new_node_y), count)
    
    if map_img[new_node[1]][new_node[0]][0] == 0:
        
        continue
    

    
    x1 = new_node[0]
    y1 = new_node[1]
    
    x2 = active_node[0]
    y2 = active_node[1]
    
    if x2 - x1 == 0.0:
        continue
    
    slope = (y2 - y1) / (x2 - x1)
    
    y_intercept = y2 - (slope * x2)
    
    low_lim = 0.98
    high_lim = 1.02
    
    obstacle_found = False
    

    for points in obstacle_map:
        
        x_point = points[0]
        y_point = points[1]
        
        if (x_point > max(active_node[0], new_node[0]) or x_point < min(active_node[0], new_node[0])) or (y_point > max(active_node[1], new_node[1]) or y_point < min(active_node[1], new_node[1])):

            continue
        
    
        if ((slope * x_point) + y_intercept) / y_point > low_lim and ((slope * x_point) + y_intercept) / y_point < high_lim:

            obstacle_found = True
            break
            
    
    if obstacle_found:

        continue
    
    map_img = cv.rectangle(map_img, (new_node[0] - 2, new_node[1] - 2), (new_node[0] + 2, new_node[1] + 2), (0, 0, 255), -1)
    
    # Add to the tree and add connection
    
    random_tree.addtotree(new_node)
    random_tree.addalink(new_node[2], active_node_id, min_temp_dist)    
    # Drawing link lines
    
    map_img =  cv.line(map_img, (int(new_node[0]), int(new_node[1])), (random_tree.location_map[active_node_id][0], random_tree.location_map[active_node_id][1]), (0, 255, 0), 1)
    

    
    x1 = goal_point[0]
    y1 = goal_point[1]
    
    x2 = new_node[0]
    y2 = new_node[1]
    
    if x2- x1 == 0.0:
        continue
    
    slope = (y2 - y1) / (x2 - x1)
    
    y_intercept = y2 - (slope * x2)
    
    low_lim = 0.98
    high_lim = 1.02
    
    obstacle_found = False
    
    for points in obstacle_map:
        
        x_point = points[0]
        y_point = points[1]
        
        if (x_point > max(goal_point[0], new_node[0]) or x_point < min(goal_point[0], new_node[0])) or (y_point > max(goal_point[1], new_node[1]) or y_point < min(goal_point[1], new_node[1])):

            continue
        
    
        if ((slope * x_point) + y_intercept) / y_point > low_lim and ((slope * x_point) + y_intercept) / y_point < high_lim:
            
            obstacle_found = True

            
            break
            
            
    if not obstacle_found:
        print("Finished Building the Rapidly-exploring Random Tree")
        path_found = True

        map_img = draw_path(map_img, new_node, goal_point)
        
cv.imwrite(sys.argv[1] + ".png", map_img)

cv.imshow("Final Output", map_img)
cv.waitKey(0)
    
cv.destroyAllWindows()