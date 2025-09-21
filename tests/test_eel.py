import pytest
import pygame
from eel.eel import Eel
from eel import config


class TestEel:

    def setup_method(self):
        pygame.init()
        self.eel = Eel(5, 5)

    def teardown_method(self):
        pygame.quit()

    def test_init_default_position(self):
        eel = Eel()
        assert eel.grid_x == 5
        assert eel.grid_y == 5
        assert eel.target_grid_x == 5
        assert eel.target_grid_y == 5

    def test_init_custom_position(self):
        eel = Eel(3, 7)
        assert eel.grid_x == 3
        assert eel.grid_y == 7
        assert eel.target_grid_x == 3
        assert eel.target_grid_y == 7

    def test_init_direction(self):
        assert self.eel.auto_direction == pygame.Vector2(1, 0)
        assert self.eel.pending_direction is None

    def test_init_movement_state(self):
        assert self.eel.move_timer == 0
        assert self.eel.first_move is True

    def test_init_body(self):
        assert self.eel.body == []
        assert self.eel.body_history == []

    def test_add_segment_empty_body(self):
        self.eel.add_segment()
        assert len(self.eel.body) == 1
        assert self.eel.body[0] == (-10, -10)

    def test_add_segment_with_history(self):
        for i in range(50):
            self.eel.body_history.append((i, i))

        initial_body_count = len(self.eel.body)
        history_length = len(self.eel.body_history)

        self.eel.add_segment()
        assert len(self.eel.body) == initial_body_count + 1

        positions_per_cell = int(config.MOVE_INTERVAL * config.FPS)
        new_segment_index = initial_body_count * positions_per_cell + positions_per_cell

        if history_length > new_segment_index:
            assert self.eel.body[-1] != (-10, -10)
        else:
            assert self.eel.body[-1] == (-10, -10)

    def test_get_head_position(self):
        self.eel.grid_x = 5.7
        self.eel.grid_y = 3.2
        head_pos = self.eel.get_head_position()
        assert head_pos == (6, 3)

    def test_set_pending_direction(self):
        new_direction = pygame.Vector2(0, -1)
        self.eel.set_pending_direction(new_direction)
        assert self.eel.pending_direction == new_direction

    def test_is_valid_direction_change_valid(self):
        self.eel.auto_direction = pygame.Vector2(1, 0)
        new_direction = pygame.Vector2(0, 1)
        assert self.eel._is_valid_direction_change(new_direction) is True

    def test_is_valid_direction_change_invalid(self):
        self.eel.auto_direction = pygame.Vector2(1, 0)
        opposite_direction = pygame.Vector2(-1, 0)
        assert self.eel._is_valid_direction_change(opposite_direction) is False

    def test_is_out_of_bounds_inside(self):
        self.eel.target_grid_x = 5
        self.eel.target_grid_y = 5
        assert self.eel.is_out_of_bounds() is False

    def test_is_out_of_bounds_outside_left(self):
        self.eel.target_grid_x = -1
        self.eel.target_grid_y = 5
        assert self.eel.is_out_of_bounds() is True

    def test_is_out_of_bounds_outside_right(self):
        self.eel.target_grid_x = 11
        self.eel.target_grid_y = 5
        assert self.eel.is_out_of_bounds() is True

    def test_is_out_of_bounds_outside_top(self):
        self.eel.target_grid_x = 5
        self.eel.target_grid_y = -1
        assert self.eel.is_out_of_bounds() is True

    def test_is_out_of_bounds_outside_bottom(self):
        self.eel.target_grid_x = 5
        self.eel.target_grid_y = 11
        assert self.eel.is_out_of_bounds() is True

    def test_check_self_collision_no_body(self):
        assert self.eel.check_self_collision() is False

    def test_check_self_collision_with_body_no_collision(self):
        self.eel.body = [(3, 3), (2, 3), (1, 3)]
        self.eel.grid_x = 5.0
        self.eel.grid_y = 5.0
        assert self.eel.check_self_collision() is False

    def test_check_self_collision_with_collision(self):
        self.eel.body = [(5, 5), (4, 5), (3, 5)]
        self.eel.grid_x = 5.0
        self.eel.grid_y = 5.0
        assert self.eel.check_self_collision() is True

    def test_get_pixel_position(self):
        grid_bounds = pygame.Rect(100, 100, 550, 550)
        self.eel.grid_x = 2
        self.eel.grid_y = 3

        pixel_pos = self.eel.get_pixel_position(grid_bounds)
        expected_x = 100 + (2 * config.CELL_SIZE) + (config.CELL_SIZE // 2)
        expected_y = 100 + (3 * config.CELL_SIZE) + (config.CELL_SIZE // 2)

        assert pixel_pos.x == expected_x
        assert pixel_pos.y == expected_y

    def test_limit_history(self):
        for i in range(1000):
            self.eel.body_history.append((i, i))

        self.eel.body = [(1, 1), (2, 2), (3, 3)]

        self.eel._limit_history()

        positions_per_cell = int(config.MOVE_INTERVAL * config.FPS)
        max_history = len(self.eel.body) * positions_per_cell + 100
        assert len(self.eel.body_history) <= max_history

    def test_methods_exist(self):
        methods = ['add_segment', 'update_movement', 'get_head_position',
                  'check_self_collision', 'is_out_of_bounds', 'set_pending_direction',
                  'get_pixel_position', 'draw']

        for method in methods:
            assert hasattr(self.eel, method)
            assert callable(getattr(self.eel, method))