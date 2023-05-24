import pytest
from unittest.mock import MagicMock, patch, Mock
from src.kdtree import KDTree, Node, c1rcle


@pytest.fixture
def circles():
    return [[(0.9143145161290325, 4.603571428571429), 2], [(2, 2), 2], [(0, 0), 1], [(0, 1), 3]]

@pytest.fixture
def mock_node():
    node = MagicMock()
    node.left = None
    node.right = None
    return node

points = [(0, 5), (0.1, 0.9), (1.3, 0.5), (1.5, 3), (2.5, 3), (4, 2), (5, 1)]
@pytest.fixture
def kdtree():
    return KDTree(points)

@pytest.fixture
def points_amount():
    return len(points)

def test_build_kdtree(mock_node, kdtree):
    kdtree.build_kdtree = MagicMock(return_value=mock_node)
    result = kdtree.build_kdtree([(0, 5), (0.1, 0.9), (1.3, 0.5)])
    assert result == mock_node
    kdtree.build_kdtree.assert_called_once_with([(0, 5), (0.1, 0.9), (1.3, 0.5)])

def test_is_point_in_circle(mock_node, kdtree):
    kdtree._check_point_in_circle = MagicMock(return_value=True)
    result = kdtree.is_point_in_circle((2, 2), 2, (1.5, 3))
    assert result is True
    kdtree._check_point_in_circle.assert_called_once_with(kdtree.root, (2, 2), 2, (1.5, 3), 0)

def test_inorder_traversal(kdtree, capsys):
    kdtree._inorder_recursive = MagicMock()
    kdtree.inorder_traversal()
    kdtree._inorder_recursive.assert_called_once_with(kdtree.root)
    captured = capsys.readouterr()
    assert captured.out == ""

# @patch('__main__.circles', new=[[(2, 2), 2]])
def test_err(kdtree, circles):
    with patch('test.circles', new=[[[(None, None), None]]]):
        print(f"TEST. {circles[0][0]=}, {circles[0][1]=}")
        er = kdtree.traverse_and_check_circle(c1rcle[0][0], c1rcle[0][1])
        # assert dots_in_c == [(1.5, 3), (1.3, 0.5), (4, 2), (2.5, 3)]
        assert er =="Error, center or raduis is empty", "Error do not happen"

def test_go_through_tree(kdtree):
    dots_in_c = kdtree.traverse_and_check_circle((2,2), 2)
    assert dots_in_c == [(1.5, 3), (1.3, 0.5), (4, 2), (2.5, 3)]


def test_postorder_traversal(kdtree, capsys):
    kdtree._postorder_recursive = MagicMock()
    kdtree.postorder_traversal()
    kdtree._postorder_recursive.assert_called_once_with(kdtree.root)

    captured = capsys.readouterr()
    assert captured.out == ""

def test_traverse_and_check_circle(mock_node, kdtree):
    kdtree.draw_dots = MagicMock()
    kdtree.draw_circle = MagicMock()

    kdtree._traverse_and_check_circle_recursive = Mock(wraps=kdtree._traverse_and_check_circle_recursive)

    center = (2, 2)
    radius = 2

    kdtree.traverse_and_check_circle(center, radius)

    assert 14 == kdtree._traverse_and_check_circle_recursive.call_count
    # print(f"{count=}")

    # kdtree._traverse_and_check_circle_recursive.assert_called_once_with(kdtree.root, center, radius, kdtree._traverse_and_check_circle_recursive)

    # node = Node((5,1),2, None, None)
    # ax = MagicMock()

    # Additional assertions or verifications based on the expected behavior
    # assert_func = getattr(kdtree._traverse_and_check_circle_recursive, "assert_not_called_with")
    # assert_func(node, center, 2, ax)



