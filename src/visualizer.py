from loguru import logger
import pygame

class TemperatureController:
    
    def __init__(self, initial_temperature):
        # Temperature variable.
        self.temperature = initial_temperature
        
        # Variables to keep track of if the control keys have been released after being pressed.
        self.up_released = True
        self.down_released = True
    
    def get_temperature(self):
        return self.temperature
    
    def handle_inputs(self, keys_pressed):
        # Reset released flags.
        if not keys_pressed[pygame.K_UP]:
            self.up_released = True
        if not keys_pressed[pygame.K_DOWN]:
            self.down_released = True
        
        # Check if temperature needs to be updated.
        if keys_pressed[pygame.K_UP] and self.up_released:
            self.temperature *= 2
            self.up_released = False
        if keys_pressed[pygame.K_DOWN] and self.down_released:
            self.temperature /= 2
            self.down_released = False

def window(resolution=(1920, 1080), simulation=None):
    if simulation is None:
        logger.critical("Simulation cannot be None! Please supply a simulation.")
        return
    
    # Initialize pygame.
    pygame.init()
    
    # Initialize font.
    font = pygame.freetype.SysFont("Courier New", 20)
    
    # Initialize graph fonts.
    small_font = pygame.freetype.SysFont("Courier New", 15)
    big_font = pygame.freetype.SysFont("Courier New", 20)
    
    
    # Initialize display.
    display = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Ising Model Visualization")
    
    # Simulation parameters.
    temperature_controller = TemperatureController(initial_temperature=10)
    
    # Main loop.
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Get keys pressed.
        keys_pressed = pygame.key.get_pressed()
        
        # Close window if escape is pressed.
        if keys_pressed[pygame.K_ESCAPE]:
            running = False
        
        # Handle temperature control.
        temperature_controller.handle_inputs(keys_pressed)
        temperature = temperature_controller.get_temperature()
        
        # Clear display.
        display.fill((0, 0, 0))
        
        # Render world.
        simulation.update(temperature=temperature)
        simulation.render(display, font, resolution)
        
        # Get average spin.
        average_spin = simulation.get_average_spin()
        
        # Render debug text.
        render_text_topleft(display, font, f"Temperature: {temperature}", (10, 10), (255, 0, 0))
        render_text_topleft(display, font, f"Average spin: {average_spin:.2f}", (10, 30), (255, 0, 0))
        
        render_graph(display, small_font, big_font, x=range(len(simulation.average_spin_over_time)), y=simulation.average_spin_over_time, position=(20, resolution[1] / 2 + 100), size=(400, 200), axes_color=(255, 255, 255), raw_data_color=(0, 0, 255), moving_average_color=(255, 0, 0), title="Average Spin over Time", x_axis_label="Time", y_axis_label="Average Spin")
        
        # Update display.
        pygame.display.flip()
        
        # Tick clock.
        clock.tick(30)
    
    # Quit pygame.
    pygame.quit()

def render_text_topleft(display, font, text, position, color):
    font.render_to(display, position, text, color)

def render_text_center(display, font, text, color, position, rotation=0):
    # Get text render rect.
    text_surface, rect = font.render(text, False, color)
    
    # Render text to separate surface to prevent white rectangle.
    surf = pygame.Surface((rect[2], rect[3]))
    font.render_to(surf, (0, 0), text, color)
    
    # Rotate surface if applicable.
    if rotation != 0:
        surf = pygame.transform.rotate(surf, rotation)
    
    # Blit text to screen.
    if rotation % 180 == 90:
        display.blit(surf, (position[0] - text_surface.get_height() / 2, position[1] - text_surface.get_width() / 2))
    else:
        display.blit(surf, (position[0] - text_surface.get_width() / 2, position[1] - text_surface.get_height() / 2))

def render_graph(surface, small_font, big_font, x, y, position, size, **kwargs):
    # Render axes.
    axes_color = kwargs["axes_color"] if "axes_color" in kwargs else (255, 255, 255)
    bottomleft = (position[0] + 10, position[1] + 10)
    pygame.draw.line(surface, axes_color, bottomleft, (bottomleft[0], bottomleft[1] - size[1] + 30))
    pygame.draw.line(surface, axes_color, bottomleft, (bottomleft[0] + size[0] - 10, bottomleft[1]))
    
    # Render axis labels and graph title.
    graph_title = kwargs["title"] if "title" in kwargs else "Graph Title"
    render_text_center(surface, big_font, graph_title, axes_color, (bottomleft[0] + (size[0] / 2), bottomleft[1] - size[1] + 10))
    x_axis_label = kwargs["x_axis_label"] if "x_axis_label" in kwargs else "X Axis"
    render_text_center(surface, small_font, x_axis_label, axes_color, (bottomleft[0] + (size[0] / 2), bottomleft[1] + 25))
    y_axis_label = kwargs["y_axis_label"] if "y_axis_label" in kwargs else "Y Axis"
    render_text_center(surface, small_font, y_axis_label, axes_color, (bottomleft[0] - 15, bottomleft[1] - (size[1] / 2) + 10), rotation=90)
    
    # Get data bounds.
    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)
    
    # Don't render data if there is no x range.
    if min_x == max_x:
        return
    
    # If there is no y range, invent one, as the y value is constant.
    if min_y == max_y:
        if min_y == 0:
            min_y = -1
            max_y = +1
        else:
            min_y *= 0.9
            max_y *= 1.1
    
    # Render y axis ticks.
    render_text_center(surface, small_font, f"{max_y:.2f}", axes_color, (bottomleft[0] - 12, bottomleft[1] - size[1] + 30), rotation=90)
    pygame.draw.line(surface, axes_color, (bottomleft[0], bottomleft[1] - size[1] + 30), (bottomleft[0] - 5, bottomleft[1] - size[1] + 30))
    render_text_center(surface, small_font, f"{min_y:.2f}", axes_color, (bottomleft[0] - 12, bottomleft[1] - 0), rotation=90)
    pygame.draw.line(surface, axes_color, (bottomleft[0], bottomleft[1]), (bottomleft[0] - 5, bottomleft[1]))
    
    # Render x axis ticks.
    tick_interval = max(50, ((max_x - min_x) // 400) * 100)
    xticks = list(range(0, max_x, tick_interval)) + [max_x]
    for xtick in xticks:
        screen_x = bottomleft[0] + (xtick / max_x) * (size[0] - 10)
        screen_y = bottomleft[1]
        
        pygame.draw.line(surface, axes_color, (screen_x, screen_y), (screen_x, screen_y + 5))
        render_text_center(surface, small_font, f"{xtick}", axes_color, (screen_x, screen_y + 13))
    
    # Transform all raw data points to screen points.
    raw_data_screen_points = []
    for px, py in zip(x, y):
        screen_x = bottomleft[0] + (size[0] - 10) * (px - min_x) / (max_x - min_x)
        screen_y = bottomleft[1] - (size[1] - 30) * (py - min_y) / (max_y - min_y)
        raw_data_screen_points.append((screen_x, screen_y))
    
    # Render raw data lines.
    raw_data_color = kwargs["raw_data_color"] if "raw_data_color" in kwargs else (255, 255, 255)
    for index in range(len(raw_data_screen_points)):
        if index == 0:
            continue
        
        pygame.draw.line(surface, raw_data_color, raw_data_screen_points[index - 1], raw_data_screen_points[index])
    
    # Calculate moving average data points.
    filter_size = min(len(x), 50)
    moving_average_y = []
    for index in range(len(y)):
        if index == 0:
            moving_average_y.append(y[index])
            continue
        
        start = max(0, index - filter_size)
        end = index
        moving_average_y.append(sum(y[start:end]) / (end - start))
    
    # Transform moving average data points to screen points.
    moving_average_screen_points = []
    for px, py in zip(x, moving_average_y):
        screen_x = bottomleft[0] + (size[0] - 10) * (px - min_x) / (max_x - min_x)
        screen_y = bottomleft[1] - (size[1] - 30) * (py - min_y) / (max_y - min_y)
        moving_average_screen_points.append((screen_x, screen_y))
    
    # Render moving average lines.
    moving_average_color = kwargs["moving_average_color"] if "moving_average_color" in kwargs else (255, 255, 255)
    for index in range(len(moving_average_screen_points)):
        if index == 0:
            continue
        
        pygame.draw.line(surface, moving_average_color, moving_average_screen_points[index - 1], moving_average_screen_points[index])
