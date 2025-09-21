import pytest
import pygame
from eel.grid import Grid


class TestGrid:

    def setup_method(self):
        pygame.init()
        self.screen_center = (640, 360)
        self.grid = Grid(self.screen_center)

    def teardown_method(self):
        pygame.quit()

    def test_init(self):
        assert self.grid.screen_center == self.screen_center
        assert self.grid.bounds is not None

    def test_create_bounds(self):
        assert self.grid.bounds.width == 604
        assert self.grid.bounds.height == 604
        assert self.grid.bounds.center == self.screen_center

    def test_get_bounds(self):
        bounds = self.grid.get_bounds()
        assert bounds == self.grid.bounds
        assert isinstance(bounds, pygame.Rect)

    def test_bounds_dimensions(self):
        bounds = self.grid.get_bounds()
        assert bounds.width == 604
        assert bounds.height == 604

    def test_bounds_center(self):
        bounds = self.grid.get_bounds()
        assert bounds.center == self.screen_center

    def test_draw_method_exists(self):
        assert hasattr(self.grid, 'draw')
        assert callable(getattr(self.grid, 'draw'))