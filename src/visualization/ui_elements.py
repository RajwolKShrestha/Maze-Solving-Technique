"""Reusable UI widgets for the maze visualizer."""

from __future__ import annotations

from dataclasses import dataclass

try:
    import pygame
except ImportError:  # pragma: no cover - runtime guard for non-graphical environments
    pygame = None

from src.core.constants import COLORS


@dataclass(frozen=True)
class Button:
    """Simple rectangular button with text label."""

    x: int
    y: int
    width: int
    height: int
    label: str
    fill_color: tuple[int, int, int] = COLORS["gray"]
    text_color: tuple[int, int, int] = COLORS["black"]

    def contains(self, pos: tuple[int, int]) -> bool:
        px, py = pos
        return self.x <= px <= self.x + self.width and self.y <= py <= self.y + self.height

    def draw(self, screen, font, active: bool = False) -> None:
        if pygame is None:
            raise RuntimeError("pygame is required for drawing UI widgets")

        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.fill_color, rect, border_radius=8)
        border_color = COLORS["white"] if active else COLORS["dark_gray"]
        pygame.draw.rect(screen, border_color, rect, width=2, border_radius=8)

        text_surface = font.render(self.label, True, self.text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)


class AlgorithmSelector:
    """Horizontal algorithm selector made of buttons."""

    def __init__(self, algorithms: list[str], x: int, y: int, button_width: int = 112, gap: int = 8):
        self.algorithms = algorithms
        self.buttons = [
            Button(x + index * (button_width + gap), y, button_width, 34, algorithm)
            for index, algorithm in enumerate(algorithms)
        ]
        self.selected_index = 0

    @property
    def selected_algorithm(self) -> str:
        return self.algorithms[self.selected_index]

    def handle_click(self, pos: tuple[int, int]) -> str | None:
        for index, button in enumerate(self.buttons):
            if button.contains(pos):
                self.selected_index = index
                return self.selected_algorithm
        return None

    def draw(self, screen, font) -> None:
        for index, button in enumerate(self.buttons):
            button.draw(screen, font, active=index == self.selected_index)


class PlaybackControls:
    """Play/pause/reset controls for animation playback."""

    def __init__(self, x: int, y: int):
        self.play_button = Button(x, y, 86, 34, "Play")
        self.pause_button = Button(x + 96, y, 86, 34, "Pause")
        self.reset_button = Button(x + 192, y, 86, 34, "Reset")

    def handle_click(self, pos: tuple[int, int]) -> str | None:
        if self.play_button.contains(pos):
            return "play"
        if self.pause_button.contains(pos):
            return "pause"
        if self.reset_button.contains(pos):
            return "reset"
        return None

    def draw(self, screen, font, is_playing: bool) -> None:
        self.play_button.draw(screen, font, active=is_playing)
        self.pause_button.draw(screen, font, active=not is_playing)
        self.reset_button.draw(screen, font)


class MetricsPanel:
    """Render solver metrics and algorithm notes."""

    def __init__(self, x: int, y: int, width: int = 250):
        self.x = x
        self.y = y
        self.width = width
        self.metrics: dict[str, str] = {}

    def update(self, solver) -> None:
        self.metrics = {
            "Algorithm": solver.name,
            "Steps": str(solver.steps),
            "Path Length": str(len(solver.path)),
            "Cells Explored": str(len(solver.explored)),
            "Time Complexity": solver.get_time_complexity(),
        }

    def draw(self, screen, font) -> None:
        if pygame is None:
            raise RuntimeError("pygame is required for drawing UI widgets")

        panel_rect = pygame.Rect(self.x, self.y, self.width, 220)
        pygame.draw.rect(screen, COLORS["white"], panel_rect, border_radius=12)
        pygame.draw.rect(screen, COLORS["dark_gray"], panel_rect, width=2, border_radius=12)

        title = font.render("Metrics", True, COLORS["black"])
        screen.blit(title, (self.x + 12, self.y + 12))

        y_offset = self.y + 48
        for key, value in self.metrics.items():
            line = font.render(f"{key}: {value}", True, COLORS["black"])
            screen.blit(line, (self.x + 12, y_offset))
            y_offset += 26


class ComparisonPanel:
    """Display a compact algorithm comparison table."""

    def __init__(self, x: int, y: int, width: int = 250):
        self.x = x
        self.y = y
        self.width = width
        self.rows: list[tuple[str, str, str, str]] = []

    def update(self, snapshots) -> None:
        self.rows = [
            (
                snapshot.name,
                str(snapshot.path_length),
                str(snapshot.steps),
                f"{snapshot.elapsed_ms:.1f}ms",
            )
            for snapshot in snapshots
        ]

    def draw(self, screen, font) -> None:
        if pygame is None:
            raise RuntimeError("pygame is required for drawing UI widgets")

        panel_rect = pygame.Rect(self.x, self.y, self.width, 240)
        pygame.draw.rect(screen, COLORS["white"], panel_rect, border_radius=12)
        pygame.draw.rect(screen, COLORS["dark_gray"], panel_rect, width=2, border_radius=12)

        title = font.render("Comparison", True, COLORS["black"])
        screen.blit(title, (self.x + 12, self.y + 12))

        headers = font.render("Alg   Path  Steps  Time", True, COLORS["dark_gray"])
        screen.blit(headers, (self.x + 12, self.y + 40))

        y_offset = self.y + 70
        for name, path_length, steps, elapsed_ms in self.rows[:6]:
            text = font.render(f"{name:<10} {path_length:<5} {steps:<5} {elapsed_ms}", True, COLORS["black"])
            screen.blit(text, (self.x + 12, y_offset))
            y_offset += 26