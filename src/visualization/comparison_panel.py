"""Panel that renders algorithm comparison results."""

from __future__ import annotations

try:
    import pygame
except ImportError:  # pragma: no cover - runtime guard
    pygame = None

from src.core.constants import COLORS


class ComparisonPanel:
    """Render side-by-side algorithm comparison snapshots."""

    def __init__(self, x: int, y: int, width: int = 250):
        self.x = x
        self.y = y
        self.width = width
        self.snapshots: list = []

    def update(self, snapshots: list) -> None:
        self.snapshots = snapshots

    def draw(self, screen, font) -> None:
        if pygame is None:
            raise RuntimeError("pygame is required for drawing UI widgets")

        panel_rect = pygame.Rect(self.x, self.y, self.width, 260)
        pygame.draw.rect(screen, COLORS["white"], panel_rect, border_radius=12)
        pygame.draw.rect(screen, COLORS["dark_gray"], panel_rect, width=2, border_radius=12)

        title = font.render("Comparison", True, COLORS["black"])
        screen.blit(title, (self.x + 12, self.y + 12))

        y_offset = self.y + 46
        for snapshot in self.snapshots[:5]:
            line = font.render(
                f"{snapshot.name}: {snapshot.path_length} steps={snapshot.steps} {snapshot.elapsed_ms:.1f}ms",
                True,
                COLORS["black"],
            )
            screen.blit(line, (self.x + 12, y_offset))
            y_offset += 28