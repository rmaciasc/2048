from dataclasses import dataclass
import pygame
import random
from src import Ui, Board


@dataclass
class Game:
    timer = pygame.time.Clock()
    run: bool = True
    screen = pygame.display.set_mode([Ui.WIDTH, Ui.HEIGHT])
    spawn_new: bool = True
    game_over: bool = False
    init_count: int = 0
    direction: str = ""
    score: int = 0
    file = open("high_score.txt", "a+")
    file.seek(0)
    initial_hi = int(file.readline())
    file.close()
    high_score: int = initial_hi

    def new_pieces(self, board_values: Board.board_values) -> tuple([Board.board_values, bool]):
        full = False
        counter = 0
        while any(0 in row for row in board_values) and counter < 1:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            if board_values[row][col] == 0:
                counter += 1
                board_values[row][col] = 2
        if counter < 1:
            full = True

        return board_values, full

    def take_turn(self, board_values: Board.board_values) -> Board.board_values:
        merged = [[False for _ in range(4)] for _ in range(4)]

        if self.direction == "UP":
            for i in range(4):
                for j in range(4):
                    shift = 0
                    if i > 0:
                        for q in range(i):
                            q
                            if board_values[q][j] == 0:
                                shift += 1
                        if shift > 0:
                            board_values[i - shift][j] = board_values[i][j]
                            board_values[i][j] == 0
                        if (
                            board_values[i - shift - 1][j] == board_values[i - shift][j]
                            and not merged[i - shift][j]
                            and not merged[i - shift - 1][j]
                        ):
                            board_values[i - shift - 1][j] *= 2
                            self.score += board_values[i - shift - 1][j]
                            board_values[i - shift][j] = 0
                            merged[i - shift - 1][j] = True

        if self.direction == "DOWN":
            for i in range(3):
                for j in range(4):
                    shift = 0
                    for q in range(i + 1):
                        if board_values[3 - q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board_values[2 - i + shift][j] = board_values[2 - i][j]
                        board_values[2 - i][j] = 0
                    if 3 - i + shift <= 3:
                        if (
                            board_values[2 - i + shift][j] == board_values[3 - i + shift][j]
                            and not merged[2 - i + shift][j]
                            and not merged[3 - i + shift][j]
                        ):
                            board_values[3 - i + shift][j] *= 2
                            self.score += board_values[3 - i + shift][j]
                            board_values[2 - i + shift][j] = 0
                            merged[3 - i + shift][j] = True

        if self.direction == "LEFT":
            for i in range(4):
                for j in range(4):
                    shift = 0
                    for q in range(j):
                        if board_values[i][q] == 0:
                            shift += 1
                    if shift > 0:
                        board_values[i][j - shift] = board_values[i][j]
                        board_values[i][j] = 0
                    if (
                        board_values[i][j - shift] == board_values[i][j - shift - 1]
                        and not merged[i][j - shift]
                        and not merged[i][j - 1 - shift]
                    ):
                        board_values[i][j - shift - 1] *= 2
                        self.score += board_values[i][j - shift - 1]
                        board_values[i][j - shift] = 0
                        merged[i][j - shift - 1] = True

        if self.direction == "RIGHT":
            for i in range(4):
                for j in range(4):
                    shift = 0
                    for q in range(j):
                        if board_values[i][3 - q] == 0:
                            shift += 1
                    if shift > 0:
                        board_values[i][3 - j + shift] = board_values[i][3 - j]
                        board_values[i][3 - j] = 0
                    if 4 - j + shift <= 3:
                        if (
                            board_values[i][3 - j + shift] == board_values[i][4 - j + shift]
                            and not merged[i][4 - j + shift]
                            and not merged[i][3 - j + shift]
                        ):
                            board_values[i][4 - j + shift] *= 2
                            self.score += board_values[i][4 - j + shift]
                            board_values[i][3 - j + shift] = 0
                            merged[i][4 - j + shift] = True

        return board_values

    def init(self) -> None:
        pygame.init()
        pygame.display.set_caption("2048")
        self.screen.fill("gray")
        board = Board(self.screen)

        while self.run:
            self.timer.tick(Ui.FPS)

            board.draw_board(self.score, self.high_score)
            board.draw_pieces()

            if self.spawn_new or self.init_count < 2:
                board.board_values, self.game_over = self.new_pieces(board.board_values)
                self.spawn_new = False
                self.init_count += 1

            if self.direction != "":
                board.board_values = self.take_turn(board.board_values)
                self.direction = ""
                self.spawn_new = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.direction = "UP"
                    if event.key == pygame.K_DOWN:
                        self.direction = "DOWN"
                    if event.key == pygame.K_LEFT:
                        self.direction = "LEFT"
                    if event.key == pygame.K_RIGHT:
                        self.direction = "RIGHT"

            if self.score > self.high_score:
                self.high_score = self.score

            pygame.display.flip()

        pygame.quit()
