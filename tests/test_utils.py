"""Tests for pipeline/utils.py — runs without Ollama or real data."""

import sys
import os

# Allow imports from pipeline/ when running from repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pipeline'))

import numpy as np
import pytest
from utils import is_trivial_response, parse_llm_category_lines


# ── is_trivial_response ───────────────────────────────────────────────────────

class TestIsTrivialResponse:
    def test_nan_is_trivial(self):
        assert is_trivial_response(float('nan')) is True

    def test_none_is_trivial(self):
        assert is_trivial_response(None) is True

    def test_numpy_nan_is_trivial(self):
        assert is_trivial_response(np.nan) is True

    @pytest.mark.parametrize("text", [
        "no", "No", "NO", "nope", "n/a", "N/A", "nothing",
        "none", "not really", "nah", "nada", "idk",
        "dont know", "not sure", "no idea", "",
    ])
    def test_trivial_words(self, text):
        assert is_trivial_response(text) is True

    def test_single_char_is_trivial(self):
        assert is_trivial_response("x") is True

    def test_two_chars_is_trivial(self):
        assert is_trivial_response("ok") is True

    @pytest.mark.parametrize("text", [
        "I love the daily rewards",
        "Better matchmaking would help",
        "The graphics are stunning",
        "More boosters please",
    ])
    def test_substantive_responses(self, text):
        assert is_trivial_response(text) is False

    def test_punctuation_stripped_before_check(self):
        # "no." should still be trivial after punctuation is stripped
        assert is_trivial_response("no.") is True

    def test_whitespace_only_is_trivial(self):
        assert is_trivial_response("   ") is True


# ── parse_llm_category_lines ─────────────────────────────────────────────────

class TestParseLlmCategoryLines:
    def test_basic_categories(self):
        output = "Graphics & Visuals\nRewards & Progression"
        result = parse_llm_category_lines(output)
        assert result == ["Graphics & Visuals", "Rewards & Progression"]

    def test_strips_bullet_prefixes(self):
        output = "- Graphics & Visuals\n• Rewards\n* Sound Design"
        result = parse_llm_category_lines(output)
        assert result == ["Graphics & Visuals", "Rewards", "Sound Design"]

    def test_strips_number_prefixes(self):
        output = "1. Graphics\n2. Sound\n3. Gameplay"
        result = parse_llm_category_lines(output)
        assert result == ["Graphics", "Sound", "Gameplay"]

    def test_max_categories_respected(self):
        output = "Graphics & Visuals\nRewards\nMatchmaking\nSound Design\nGameplay"
        result = parse_llm_category_lines(output, max_categories=3)
        assert len(result) == 3

    def test_empty_output_returns_other(self):
        assert parse_llm_category_lines("") == ["Other"]

    def test_blank_lines_skipped(self):
        output = "\nGraphics & Visuals\n\nRewards\n"
        result = parse_llm_category_lines(output)
        assert result == ["Graphics & Visuals", "Rewards"]

    def test_very_long_line_skipped(self):
        long_line = "A" * 61
        output = f"{long_line}\nGraphics"
        result = parse_llm_category_lines(output)
        assert result == ["Graphics"]

    def test_very_short_line_skipped(self):
        output = "ab\nGraphics & Visuals"
        result = parse_llm_category_lines(output)
        assert result == ["Graphics & Visuals"]

    def test_single_valid_category(self):
        output = "Overall Enjoyment"
        result = parse_llm_category_lines(output)
        assert result == ["Overall Enjoyment"]
