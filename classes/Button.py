import pygame
from settings import SCREEN, FONT, GRID_COLOR, BACKGROUND, CELL_COLOR


class Button:
    def __init__(self, rect, text, text_size, command=None):
        """Create and draw button on screen"""
        self.rect = rect
        self.x, self.y, self.width, self.height = rect
        self.text = text
        self.text_size = text_size
        self.command = command
        self.active_color = GRID_COLOR
        self.inactive_color = BACKGROUND

    def print_text(self, font_color=CELL_COLOR, font=FONT):
        """Prints text on button"""
        font = pygame.font.Font(font, self.text_size)
        text = font.render(self.text, True, font_color)
        x = self.x + (self.width - text.get_width()) // 2
        y = self.y + (self.height - text.get_height()) // 2
        SCREEN.blit(text, (x, y))

    def draw(self):
        """Draws button and text on it"""
        if self.collide():
            pygame.draw.rect(SCREEN, self.active_color, self.rect)
            self.click()
        else:
            pygame.draw.rect(SCREEN, self.inactive_color, self.rect)

        self.print_text()

    def collide(self):
        """Check if cursor collides with button"""
        x, y = pygame.mouse.get_pos()
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            return True
        return False

    def click(self):
        """If button is clicked - command()"""
        if self.command is None:
            return
        if self.collide() and pygame.mouse.get_pressed()[0]:
            self.command()
