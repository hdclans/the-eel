import pytest
import pygame
from unittest.mock import patch
from eel.food import Food
from eel import config


class TestFood:

    def setup_method(self):
        pygame.init()
        self.food = Food()

    def teardown_method(self):
        pygame.quit()

    def test_init(self):
        assert hasattr(self.food, 'x')
        assert hasattr(self.food, 'y')
        assert 0 <= self.food.x <= 10
        assert 0 <= self.food.y <= 10

    def test_get_position(self):
        self.food.x = 3
        self.food.y = 7
        position = self.food.get_position()
        assert position == (3, 7)

    @patch('random.randint')
    def test_generate_without_avoid_positions(self, mock_randint):
        mock_randint.side_effect = [4, 6]

        self.food.generate()

        assert self.food.x == 4
        assert self.food.y == 6
        assert mock_randint.call_count == 2

    @patch('random.randint')
    def test_generate_with_avoid_positions_no_conflict(self, mock_randint):
        mock_randint.side_effect = [4, 6]
        avoid_positions = [(1, 1), (2, 2), (3, 3)]

        self.food.generate(avoid_positions)

        assert self.food.x == 4
        assert self.food.y == 6

    @patch('random.randint')
    def test_generate_with_avoid_positions_with_conflict(self, mock_randint):
        mock_randint.side_effect = [3, 3, 5, 7]
        avoid_positions = [(3, 3), (1, 1)]

        self.food.generate(avoid_positions)

        assert self.food.x == 5
        assert self.food.y == 7

    def test_generate_position_range(self):
        for _ in range(100):
            self.food.generate()
            assert 0 <= self.food.x <= 10
            assert 0 <= self.food.y <= 10

    def test_generate_with_empty_avoid_list(self):
        original_x = self.food.x
        original_y = self.food.y

        self.food.generate([])

        assert 0 <= self.food.x <= 10
        assert 0 <= self.food.y <= 10

    def test_generate_with_multiple_avoid_positions(self):
        avoid_positions = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]

        for _ in range(10):
            self.food.generate(avoid_positions)
            current_pos = (self.food.x, self.food.y)
            assert current_pos not in avoid_positions

    def test_get_pixel_position_calculation(self):
        self.food.x = 2
        self.food.y = 3
        grid_bounds = pygame.Rect(100, 100, 550, 550)

        expected_x = grid_bounds.left + (self.food.x * config.CELL_SIZE) + (config.CELL_SIZE // 2)
        expected_y = grid_bounds.top + (self.food.y * config.CELL_SIZE) + (config.CELL_SIZE // 2)

        assert expected_x == 100 + (2 * 55) + 27
        assert expected_y == 100 + (3 * 55) + 27

    def test_draw_method_exists(self):
        assert hasattr(self.food, 'draw')
        assert callable(getattr(self.food, 'draw'))

    def test_position_consistency(self):
        original_pos = self.food.get_position()

        same_pos = self.food.get_position()
        assert original_pos == same_pos

    @patch('random.randint')
    def test_recursive_generation_stops(self, mock_randint):
        mock_randint.side_effect = [1, 1, 1, 1, 1, 1, 8, 9]
        avoid_positions = [(1, 1)]

        self.food.generate(avoid_positions)

        assert self.food.x == 8
        assert self.food.y == 9