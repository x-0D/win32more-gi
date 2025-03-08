"""
Pango compatibility layer for Windows.

This module provides Pango text rendering functionality for Windows applications.
"""

from enum import Enum

class Pango:
    """Pango compatibility layer."""
    class EllipsizeMode(Enum):
        """Text ellipsis modes."""
        END = 1