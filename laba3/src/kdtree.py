import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import threading
c1rcle = [[(None, None), None]]

class InteractiveCircleSelector:
    def __init__(self, radius, kdtree):
        self.fig, self.ax = plt.subplots()
        self.kdtree = kdtree
        self.radius = radius
        self.ax.scatter(*zip(*points), color='blue')
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        # plt.show()

    def on_click(self, event):
        if event.button == 1 and event.inaxes == self.ax:
            x, y = float(event.xdata), float(event.ydata)
            kdtree.traverse_and_check_circle((x,y), self.radius)





class Node:
    def __init__(self, point, depth, left=None, right=None):
        self.point = point
        self.depth = depth
        self.left = left
        self.right = right


class KDTree:
    def __init__(self, points):
        self.root = self.build_kdtree(points)
        self.dots_in_circle = []

    def build_kdtree(self, points, depth=0):
        if not points:
            return None

        k = len(points[0])
        axis = depth % k
        points.sort(key=lambda point: point[axis])
        median = len(points) // 2

        return Node(
            points[median],
            depth,
            self.build_kdtree(points[:median], depth + 1),
            self.build_kdtree(points[median + 1:], depth + 1)
        )

    def nearest_neighbor(self, target):
        nearest = None
        best_distance = float('inf')
        self._search_nearest(self.root, target, 0, nearest, best_distance)
        return nearest

    def _search_nearest(self, node, target, depth, nearest, best_distance):
        if node is None:
            return

        point = node.point
        distance = self._distance(point, target)
        if distance < best_distance:
            nearest = point
            best_distance = distance

        axis = depth % len(target)
        if target[axis] < point[axis]:
            self._search_nearest(node.left, target, depth + 1, nearest, best_distance)
        else:
            self._search_nearest(node.right, target, depth + 1, nearest, best_distance)

        if abs(point[axis] - target[axis]) < best_distance:
            if target[axis] < point[axis]:
                self._search_nearest(node.right, target, depth + 1, nearest, best_distance)
            else:
                self._search_nearest(node.left, target, depth + 1, nearest, best_distance)

    def _distance(self, point1, point2):
        return sum((p1 - p2) ** 2 for p1, p2 in zip(point1, point2))

    def is_point_in_circle(self, center, radius, point):
        return self._check_point_in_circle(self.root, center, radius, point, 0)

    def _check_point_in_circle(self, node, center, radius, point, depth):
        if node is None:
            return False

        axis = depth % len(point)
        distance = (point[axis] - center[axis]) ** 2
        if point[axis] < center[axis]:
            if distance <= radius ** 2:
                return True
            return self._check_point_in_circle(node.left, center, radius, point, depth + 1)
        else:
            if distance <= radius ** 2:
                return True
            return self._check_point_in_circle(node.right, center, radius, point, depth + 1)

    def inorder_traversal(self):
        self._inorder_recursive(self.root)

    def _inorder_recursive(self, node):
        if node:
            self._inorder_recursive(node.left)
            print(node.point, end=" ")
            self._inorder_recursive(node.right)

    def preorder_traversal(self):
        self._preorder_recursive(self.root)

    def _preorder_recursive(self, node):
        if node:
            print(node.point, end=" ")
            self._preorder_recursive(node.left)
            self._preorder_recursive(node.right)

    def postorder_traversal(self):
        self._postorder_recursive(self.root)

    def _postorder_recursive(self, node):
        if node:
            self._postorder_recursive(node.left)
            self._postorder_recursive(node.right)
            print(node.point, end=" ")
    def draw_dots(self):

        self._draw_dots_recursive(self.root)

    def _draw_dots_recursive(self, node):
        if node:
            plt.scatter(node.point[0], node.point[1], color='blue')
            self._draw_dots_recursive(node.left)
            self._draw_dots_recursive(node.right)

    def draw_circle(self, center, radius):
        circle = plt.Circle(center, radius, color='red', fill=False)
        plt.gca().add_patch(circle)

    def print_tree(self):
        self._print_tree_recursive(self.root)

    def _print_tree_recursive(self, node, indent=""):
        if node:
            if node.left:
                self._print_tree_recursive(node.left, indent + "    ")
            print(indent + str(node.point))
            if node.right:
                self._print_tree_recursive(node.right, indent + "    ")

    def traverse_and_check_circle(self, center, radius):
        if center is None or radius is None:
            return "Error, center or raduis is empty"
        print(f"Gets query for circle with {center=}, {radius=}")
        fig, ax = plt.subplots()
        # self.figures.append(fig)  # Keep track of the figures

        self.draw_dots()

        self._traverse_and_check_circle_recursive(self.root, center, radius, ax)

        # Set the title and show the figure
        self.draw_circle(center, radius)
        ax.set_title(f"Query Circle: Center={center}, Radius={radius}")
        plt.grid()
        plt.show()
        return self.dots_in_circle

    def _traverse_and_check_circle_recursive(self, node, center, radius, ax):
        if node is None:
            return

        point = node.point

        if self._distance(point, center) <= radius ** 2:
            print(f"Point {point} is inside the circle.")
            ax.scatter(point[0], point[1], color='green')  # Paint the point in green
            self.dots_in_circle.append(point)
        print(f"Checking {point=}, {center=}, distance to center: {self._distance(point, center)}, {radius ** 2=}")

        axis = abs(node.depth % len(center))
        # # if node.left is not None:
        #     print(f"Check if left child {node.left.point} should be verified. For {axis=} it should be between {center[axis]-radius=} and {center[axis]+radius=}. {node.left.point[axis]=}")
        #     if center[axis] - radius <= node.left.point[axis] <= center[axis] + radius:
        #         self._traverse_and_check_circle_recursive(node.left, center, radius, ax)
        direction = "left/right"
        if axis == 1:
            direction = "up/down"

        msg = f"check if query region {direction} for {node.point} \n"
        print(msg)
        if center[axis] - radius <= node.point[axis]:
            if node.left is not None:
                print(f"We need to check left son {node.left.point}")
            self._traverse_and_check_circle_recursive(node.left, center, radius, ax)

        if node.point[axis] <= center[axis] + radius:
            if node.right is not None:
                print(f"We need to check right son {node.right.point}")
            self._traverse_and_check_circle_recursive(node.right, center, radius, ax)

        # if node.right is not None:
        #     print(f"Check if right child {node.right.point} should be verified. For {axis=} it should be between {center[axis]-radius=} and {center[axis]+radius=}. {node.right.point[axis]=}")
        #     if center[axis] - radius <= node.right.point[axis] <= center[axis] + radius:
        #         self._traverse_and_check_circle_recursive(node.right, center, radius, ax)


# Example usage
if __name__ == "__main__":
    points = [(0,5), (0.1, 0.9), (1.3, 0.5), (1.5, 3), (2.5, 3), (4, 2), (5,1)]
    kdtree = KDTree(points)

    # kdtree.draw_dots()

    # target_point = (6, 3)
    # nearest_neighbor = kdtree.nearest_neighbor(target_point)
    # print("Target Point:", target_point)
    # print("Nearest Neighbor:", nearest_neighbor)

    center = (2, 2)
    radius = 2

    circles = [[(2, 2), 2], [(0, 0), 1], [(0, 1), 3]]
    # circles = [[(0.9143145161290325, 4.603571428571429), 2]]

    # kdtree.draw_circle(center, radius)
    points_in_circle = []
    for circle in circles:
        selector = InteractiveCircleSelector(circle[1], kdtree)
        dots_in_circle = kdtree.traverse_and_check_circle(circle[0], circle[1])
        print (f"For circle {circle} {dots_in_circle=}")


    print(f"{points_in_circle=}")

    print("Inorder Traversal:")
    kdtree.inorder_traversal()
    print()

    print("Preorder Traversal:")
    kdtree.preorder_traversal()
    print()

    print("Postorder Traversal:")
    kdtree.postorder_traversal()
    print()


    # plt.gca().set_aspect('equal', adjustable='box')
    #
    # plt.show()


    # while 1:
#     a =3

