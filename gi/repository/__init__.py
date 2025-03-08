"""
gi.repository Windows Implementation using XAML UI via win32more module.

This module provides a compatibility layer for GTK/GNOME applications on Windows
by mapping GTK/GNOME UI components to Windows UI components.
"""

# Import all submodules to make them available through gi.repository
from gi.repository.GLib import GLib
from gi.repository.Pango import Pango
from gi.repository.Gio import Gio
from gi.repository.Gtk import Gtk
from gi.repository.Adw import Adw
from gi.repository.Gdk import Gdk

# Define constants
DEBUG_COLORING = False

__all__ = [
    'GLib',
    'Pango',
    'Gio',
    'Gtk',
    'Adw',
    'Gdk',
    'DEBUG_COLORING'
]