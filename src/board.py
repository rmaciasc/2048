from dataclasses import dataclass
import pygame
from src.ui import Ui


@dataclass
class Board:
    board_values = [[0 for _ in range(4)] for _ in range(4)]
    screen: pygame.Surface

    def draw_board(self, score: int, hi_score: int) -> None:
        main_font = pygame.font.Font("freesansbold.ttf", 28)
        pygame.draw.rect(self.screen, Ui.colors["bg"], [0, 0, 400, 400], 0, 10)
        score_text = main_font.render(f"Score: {score}", True, "black")
        hi_score_text = main_font.render(f"High Score: {hi_score}", True, "black")
        self.screen.blit(score_text, (10, 410))
        self.screen.blit(hi_score_text, (10, 450))

    def draw_pieces(self):
        for i in range(len(self.board_values)):
            for j in range(len(self.board_values)):
                value = self.board_values[i][j]
                if value > 8:
                    value_color = Ui.colors["light text"]
                else:
                    value_color = Ui.colors["dark text"]
                if value <= 2048:
                    color = Ui.colors[value]
                else:
                    color = Ui.colors["other"]

                square_coord = [j * 97 + 10, i * 97 + 10, 85, 85]
                pygame.draw.rect(self.screen, color, square_coord, 0, 8)

                if value > 0:
                    value_len = len(str(value))
                    font = pygame.font.Font("freesansbold.ttf", 48 - (5 * value_len))
                    value_text = font.render(str(value), True, value_color)
                    text_rect = value_text.get_rect(center=(j * 97 + 52, i * 97 + 52))
                    self.screen.blit(value_text, text_rect)
                    pygame.draw.rect(self.screen, "black", square_coord, 2, 8)
