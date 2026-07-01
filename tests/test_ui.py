"""Tests for lightweight UI widgets."""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.visualization.ui_elements import AlgorithmSelector, Button, MetricsPanel, PlaybackControls


class DummySolver:
    name = "BFS"

    def __init__(self) -> None:
        self.steps = 12
        self.path = [(0, 0), (0, 1), (1, 1)]
        self.explored = [(0, 0), (0, 1), (1, 1), (2, 1)]

    def get_time_complexity(self) -> str:
        return "O(V + E)"


class TestUIWidgets(unittest.TestCase):
    def test_button_contains_point(self) -> None:
        button = Button(10, 20, 100, 30, "Play")
        self.assertTrue(button.contains((15, 25)))
        self.assertFalse(button.contains((200, 200)))

    def test_algorithm_selector_switches_selection(self) -> None:
        selector = AlgorithmSelector(["BFS", "DFS", "A*"], 0, 0)
        self.assertEqual(selector.selected_algorithm, "BFS")
        self.assertEqual(selector.handle_click((130, 10)), "DFS")
        self.assertEqual(selector.selected_algorithm, "DFS")

    def test_playback_controls_map_clicks_to_actions(self) -> None:
        controls = PlaybackControls(0, 0)
        self.assertEqual(controls.handle_click((10, 10)), "play")
        self.assertEqual(controls.handle_click((110, 10)), "pause")
        self.assertEqual(controls.handle_click((210, 10)), "reset")

    def test_metrics_panel_updates_from_solver(self) -> None:
        panel = MetricsPanel(0, 0)
        panel.update(DummySolver())
        self.assertEqual(panel.metrics["Algorithm"], "BFS")
        self.assertEqual(panel.metrics["Steps"], "12")
        self.assertEqual(panel.metrics["Path Length"], "3")


if __name__ == "__main__":
    unittest.main()