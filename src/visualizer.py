from loguru import logger
import pygame

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
    temperature = 10
    
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
        if keys_pressed[pygame.K_UP]:
            temperature *= 2
        if keys_pressed[pygame.K_DOWN]:
            temperature /= 2
        
        # Clear display.
        display.fill((0, 0, 0))
        
        # Render world.
        simulation.update(delta=0.1, temperature=temperature)
        simulation.render(display, font, resolution)
        
        # Get average spin.
        average_spin = simulation.get_average_spin()
        
        # Render debug text.
        render_text_topleft(display, font, f"Temperature: {temperature}", (10, 10), (255, 0, 0))
        render_text_topleft(display, font, f"Average spin: {average_spin:.2f}", (10, 30), (255, 0, 0))
        
        render_graph(display, small_font, big_font, x=range(len(simulation.average_spin_over_time)), y=simulation.average_spin_over_time, position=(20, resolution[1] / 2 + 100), size=(400, 200), axes_color=(255, 255, 255), data_color=(0, 0, 255), title="Average Spin over Time", x_axis_label="Time", y_axis_label="Average Spin")
        
        # Update display.
        pygame.display.flip()
        
        # Tick clock.
        clock.tick(5)
    
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
    render_text_center(surface, small_font, x_axis_label, axes_color, (bottomleft[0] + (size[0] / 2), bottomleft[1] + 15))
    y_axis_label = kwargs["y_axis_label"] if "y_axis_label" in kwargs else "Y Axis"
    render_text_center(surface, small_font, y_axis_label, axes_color, (bottomleft[0] - 15, bottomleft[1] - (size[1] / 2) + 10), rotation=90)
    
    # Get data bounds.
    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)
    
    # Render axis ticks.
    render_text_center(surface, small_font, f"{max_y:.2f}", axes_color, (bottomleft[0] - 12, bottomleft[1] - size[1] + 30), rotation=90)
    pygame.draw.line(surface, axes_color, (bottomleft[0], bottomleft[1] - size[1] + 30), (bottomleft[0] - 5, bottomleft[1] - size[1] + 30))
    render_text_center(surface, small_font, f"{min_y:.2f}", axes_color, (bottomleft[0] - 12, bottomleft[1] - 0), rotation=90)
    pygame.draw.line(surface, axes_color, (bottomleft[0], bottomleft[1]), (bottomleft[0] - 5, bottomleft[1]))
    
    if min_x == max_x or min_y == max_y:
        return
    
    # Transform all data points to screen point.
    screen_points = []
    for px, py in zip(x, y):
        screen_x = bottomleft[0] + (size[0] - 10) * (px - min_x) / (max_x - min_x)
        screen_y = bottomleft[1] - (size[1] - 30) * (py - min_y) / (max_y - min_y)
        screen_points.append((screen_x, screen_y))
    
    # Render lines.
    data_color = kwargs["data_color"] if "data_color" in kwargs else (255, 255, 255)
    for index in range(len(screen_points)):
        if index == 0:
            continue
        
        pygame.draw.line(surface, data_color, screen_points[index - 1], screen_points[index])
