import pytest
import pygame
from unittest.mock import patch, MagicMock
from eel.game import Game
from eel.eel import Eel
from eel.food import Food
from eel.grid import Grid
from eel import config


class TestGame:

    def setup_method(self):
        with patch('pygame.display.set_mode'), \
             patch('pygame.display.set_caption'):
            self.game = Game()

    def teardown_method(self):
        if hasattr(self, 'game'):
            self.game.running = False
        pygame.quit()

    def test_init_pygame_components(self):
        assert hasattr(self.game, 'screen')
        assert hasattr(self.game, 'clock')
        assert isinstance(self.game.clock, pygame.time.Clock)

    def test_init_game_state(self):
        assert self.game.running is True
        assert self.game.dt == 0
        assert self.game.game_started is False
        assert self.game.start_timer == 0.0
        assert self.game.start_delay == 2.0

    def test_init_game_objects(self):
        assert isinstance(self.game.eel, Eel)
        assert isinstance(self.game.food, Food)
        assert isinstance(self.game.grid, Grid)

    def test_init_center_calculation(self):
        assert hasattr(self.game, 'center')
        assert isinstance(self.game.center, pygame.Vector2)

    @patch('pygame.event.get')
    @patch('pygame.key.get_pressed')
    def test_handle_events_quit(self, mock_get_pressed, mock_event_get):
        quit_event = MagicMock()
        quit_event.type = pygame.QUIT
        mock_event_get.return_value = [quit_event]

        mock_keys = MagicMock()
        mock_keys.__getitem__.return_value = False
        mock_get_pressed.return_value = mock_keys

        self.game.handle_events()

        assert self.game.running is False

    @patch('pygame.event.get')
    @patch('pygame.key.get_pressed')
    def test_handle_events_keyboard_up(self, mock_get_pressed, mock_event_get):
        mock_event_get.return_value = []

        mock_keys = MagicMock()
        mock_keys.__getitem__.side_effect = lambda key: key == pygame.K_z
        mock_get_pressed.return_value = mock_keys

        with patch.object(self.game.eel, 'set_pending_direction') as mock_set_dir:
            self.game.handle_events()
            mock_set_dir.assert_called_once_with(pygame.Vector2(0, -1))

    @patch('pygame.event.get')
    @patch('pygame.key.get_pressed')
    def test_handle_events_keyboard_down(self, mock_get_pressed, mock_event_get):
        mock_event_get.return_value = []

        mock_keys = MagicMock()
        mock_keys.__getitem__.side_effect = lambda key: key == pygame.K_s
        mock_get_pressed.return_value = mock_keys

        with patch.object(self.game.eel, 'set_pending_direction') as mock_set_dir:
            self.game.handle_events()
            mock_set_dir.assert_called_once_with(pygame.Vector2(0, 1))

    @patch('pygame.event.get')
    @patch('pygame.key.get_pressed')
    def test_handle_events_keyboard_left(self, mock_get_pressed, mock_event_get):
        mock_event_get.return_value = []

        mock_keys = MagicMock()
        mock_keys.__getitem__.side_effect = lambda key: key == pygame.K_q
        mock_get_pressed.return_value = mock_keys

        with patch.object(self.game.eel, 'set_pending_direction') as mock_set_dir:
            self.game.handle_events()
            mock_set_dir.assert_called_once_with(pygame.Vector2(-1, 0))

    @patch('pygame.event.get')
    @patch('pygame.key.get_pressed')
    def test_handle_events_keyboard_right(self, mock_get_pressed, mock_event_get):
        mock_event_get.return_value = []

        mock_keys = MagicMock()
        mock_keys.__getitem__.side_effect = lambda key: key == pygame.K_d
        mock_get_pressed.return_value = mock_keys

        with patch.object(self.game.eel, 'set_pending_direction') as mock_set_dir:
            self.game.handle_events()
            mock_set_dir.assert_called_once_with(pygame.Vector2(1, 0))

    @patch('pygame.event.get')
    @patch('pygame.key.get_pressed')
    def test_handle_events_arrow_keys(self, mock_get_pressed, mock_event_get):
        mock_event_get.return_value = []

        mock_keys = MagicMock()
        mock_keys.__getitem__.side_effect = lambda key: key == pygame.K_UP
        mock_get_pressed.return_value = mock_keys

        with patch.object(self.game.eel, 'set_pending_direction') as mock_set_dir:
            self.game.handle_events()
            mock_set_dir.assert_called_once_with(pygame.Vector2(0, -1))

    def test_update_start_delay_not_started(self):
        self.game.dt = 0.5
        self.game.start_timer = 1.0
        self.game.game_started = False

        with patch.object(self.game.eel, 'update_movement') as mock_update:
            self.game.update()
            mock_update.assert_not_called()
            assert self.game.start_timer == 1.5

    def test_update_start_delay_finished(self):
        self.game.dt = 0.5
        self.game.start_timer = 1.8
        self.game.game_started = False

        self.game.update()

        assert self.game.start_timer == 2.3
        assert self.game.game_started is True

    def test_update_game_started(self):
        self.game.game_started = True
        self.game.dt = 0.016

        with patch.object(self.game.eel, 'update_movement') as mock_update, \
             patch.object(self.game, '_check_collisions') as mock_collisions:
            self.game.update()

            mock_update.assert_called_once_with(0.016)
            mock_collisions.assert_called_once()

    def test_check_collisions_out_of_bounds(self):
        self.game.game_started = True

        with patch.object(self.game.eel, 'is_out_of_bounds', return_value=True):
            self.game._check_collisions()
            assert self.game.running is False

    def test_check_collisions_self_collision(self):
        self.game.game_started = True

        with patch.object(self.game.eel, 'is_out_of_bounds', return_value=False), \
             patch.object(self.game.eel, 'check_self_collision', return_value=True):
            self.game._check_collisions()
            assert self.game.running is False

    def test_check_collisions_food_collision(self):
        self.game.game_started = True

        with patch.object(self.game.eel, 'is_out_of_bounds', return_value=False), \
             patch.object(self.game.eel, 'check_self_collision', return_value=False), \
             patch.object(self.game.eel, 'get_head_position', return_value=(5, 5)), \
             patch.object(self.game.food, 'get_position', return_value=(5, 5)), \
             patch.object(self.game.eel, 'add_segment') as mock_add_segment, \
             patch.object(self.game.food, 'generate') as mock_generate:

            self.game._check_collisions()

            mock_add_segment.assert_called_once()
            mock_generate.assert_called_once()

    def test_check_collisions_no_collision(self):
        self.game.game_started = True

        with patch.object(self.game.eel, 'is_out_of_bounds', return_value=False), \
             patch.object(self.game.eel, 'check_self_collision', return_value=False), \
             patch.object(self.game.eel, 'get_head_position', return_value=(5, 5)), \
             patch.object(self.game.food, 'get_position', return_value=(3, 3)):

            original_running = self.game.running
            self.game._check_collisions()
            assert self.game.running == original_running

    @patch('pygame.display.flip')
    def test_draw_method_calls(self, mock_flip):
        with patch.object(self.game.screen, 'fill') as mock_fill, \
             patch.object(self.game.grid, 'draw') as mock_grid_draw, \
             patch.object(self.game.food, 'draw') as mock_food_draw, \
             patch.object(self.game.eel, 'draw') as mock_eel_draw, \
             patch.object(self.game.grid, 'get_bounds') as mock_get_bounds:

            mock_get_bounds.return_value = pygame.Rect(0, 0, 100, 100)

            self.game.draw()

            mock_fill.assert_called_once_with(config.BG_COLOR)
            mock_grid_draw.assert_called_once_with(self.game.screen, config.CELL_SIZE)
            mock_food_draw.assert_called_once()
            mock_eel_draw.assert_called_once()
            mock_flip.assert_called_once()

    def test_run_method_exists(self):
        assert hasattr(self.game, 'run')
        assert callable(getattr(self.game, 'run'))

    def test_initial_food_avoids_snake(self):
        eel_pos = self.game.eel.get_head_position()
        food_pos = self.game.food.get_position()
        assert eel_pos != food_pos