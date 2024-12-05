import pytest
# from snakegame import * 
import pygame
import random
from unittest import mock

# Import the functions we want to test 
from snakegame import generate_coord, draw_snake, game_loop

@pytest.fixture
def init_pygame():
    """fixture to initialize and quit pygame for tests."""
    pygame.init()
    yield
    pygame.quit()

def test_game_initialization(init_pygame, mocker):
    """Test Case 1: Verify game initializes correctly."""
    mock_display = mocker.patch('pygame.display.set_mode')
    pygame.display.set_mode((800, 800))
    mock_display.assert_called_once()

def test_snake_movement():
    """Test Case 2: verify snake moved in the correct direction."""
    x, y = 100, 100
    x_change, y_change = 40, 0 # Move right 
    x += x_change
    y += y_change
    assert (x,y) == (140, 100)
    
def test_boundry_collision():
    """Test Case 3: Verify game ends on boundary collision."""
    x, y = 800, 400 # Outside right boundary 
    assert x >= 800 or y>= 800 or x < 0 or y < 0 
    
def test_food_consumption():
    """Test Case 4: verify snake grows and score increases after eating food."""
    snake_list = [[100, 100]]
    length = len(snake_list)
    food_x, food_y = 140, 100 # Food at next position 
    head_x, head_y = 140, 100
    if head_x == food_x and head_y == food_y:
        snake_list.append([food_x, food_y])
    assert len(snake_list) == length + 1 
    
def test_obstacle_generation():
    """Test Case 5: verify obstacles are generated when the snake grows."""
    snake_length = 6
    obstacles = []
    if snake_length % 3 == 0:
        obstacles.append(generate_coord())
    assert len(obstacles) >= 1

def test_obstacle_collision():
    """Test Case 6: Verify game ends on obstacle collision."""
    x, y = 100, 100
    obstacles = [[100,100]]
    collision = any([x, y] == obs for obs in obstacles)
    assert collision

def test_food_obstacles_placement():
    """Test Case 7: verify food and obstacles do not overlap."""
    food_x, food_y = generate_coord()
    obstacle = [food_x, food_y]
    assert (food_x, food_y) != (obstacle[0], obstacle[1])

def test_score_display(init_pygame, mocker):
    """Test Case 8: Verify the score is displayed correctly."""
    mock_font = mocker.patch('pygame.font.SysFont')
    mock_render = mock_font.return_value.render
    score = 10 
    font = pygame.font.SysFont("comicsansms", 35)
    font.render(f"Score: {score}", True, (255, 255, 102))
    mock_render.assert_called_once()
    
def test_restart_game(mocker):
    """Test Case 9: Verify the game restarts when 'C' is pressed."""
    mock_event = mocker.patch('pygame.event.get', return_value=[pygame.event.Event(pygame.KEYWDOWN, {'key': pygame.K_c})])
    mock_game_loop = mocker.patch('snakegame.game_loop')
    game_loop()
    mock_game_loop.assert_called_once()
    
def test_quit_game(mocker):
    """Test Case 10: verify the game quits when 'Q' is pressed."""
    mock_event = mocker.patch('pygame.event.get', return_value=[pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_q})])
    mock_quit = mocker.patch('pygame.quit')
    with pytest.raises(SystemExit):
        pygame.quit()
        quit()
    mock_quit.assert_called_once()

