"""
Compatibility layer for gi.repository.

This module contains base classes and mixins used across the gi.repository implementation.
"""

from ctypes import c_bool, c_int32
import typing

from win32more.Windows.Foundation import IReference
from win32more.Microsoft.UI.Xaml import (
    Visibility, Thickness, HorizontalAlignment, VerticalAlignment
)
from win32more.Microsoft.UI.Xaml.Controls import (
    ContentControl, Panel, Border, ToolTip, ToolTipService
)
from win32more.Microsoft.UI.Xaml.Media import SolidColorBrush
from win32more.Windows.Win32.System.WinRT import IInspectable

# Constants
Int32 = c_int32

class _WinUIControl:
    """Base class for all WinUI controls."""
    _obj = None
    
    def winui_get_obj(self):
        """Return the underlying WinUI object."""
        return self._obj

    def is_visible(self) -> bool:
        """Check if the control is visible."""
        return self._obj.Visibility == Visibility.Visible 

    def set_visible(self, visibility: bool):
        """Set the visibility of the control."""
        self._obj.Visibility = Visibility.Visible if visibility else Visibility.Collapsed


class _EventCtl:
    """Mixin for event handling functionality."""
    _events: dict = {}
    
    def __init__(self):
        """Initialize the event controller."""
        if not hasattr(self, '_events'):
            self._events = {}
    
    def _event(self, name: str):
        """Trigger an event by name."""
        event_attr = f"_event_{name}"
        if not getattr(self, event_attr, False):
            setattr(self, event_attr, True)
            event_list: typing.List[list] = self._events.get(name, None)
            if event_list is not None:
                length = len(event_list)
                print(f"[EVENTS] number of events: {length}")
                for index in range(length):
                    event = event_list[index]
                    print(f"[Event] {event=}")
                    func = event[0]
                    func(self, *event[1:])
        setattr(self, event_attr, False)
    
    def connect(self, *args):
        """Connect an event handler to an event."""
        args = list(args)
        event_name = args.pop(0)
        events_list: list = self._events.get(event_name, [])
        events_list.append(args)
        self._events[event_name] = events_list


class _ItemSetter:
    """Mixin for setting child elements."""
    def set_child(self, child):
        """Set a child element for the control."""
        if isinstance(self._obj, ContentControl):
            self._obj.Content = child.winui_get_obj()
        elif isinstance(self._obj, Panel):
            self._obj.Children.Clear()
            self._obj.Children.Append(child.winui_get_obj())
        elif isinstance(self._obj, Border):
            self._obj.Child = child.winui_get_obj()


class _TextField:
    """Mixin for text field functionality."""
    def get_text(self):
        """Get the text of the control."""
        return self._obj.Text
    
    def set_text(self, text):
        """Set the text of the control."""
        self._obj.Text = text

    def set_placeholder_text(self, text):
        """Set the placeholder text of the control."""
        self._obj.PlaceholderText = text


class _Margin:
    """Mixin for margin functionality."""
    def set_margin_start(self, value):
        """Set the start margin of the control."""
        margin = self._obj.Margin
        margin.Left = value
        self._obj.Margin = margin
    
    def set_margin_end(self, value):
        """Set the end margin of the control."""
        margin = self._obj.Margin
        margin.Right = value
        self._obj.Margin = margin
    
    def set_margin_top(self, value):
        """Set the top margin of the control."""
        margin = self._obj.Margin
        margin.Top = value
        self._obj.Margin = margin
    
    def set_margin_bottom(self, value):
        """Set the bottom margin of the control."""
        margin = self._obj.Margin
        margin.Bottom = value
        self._obj.Margin = margin


class _StyleContext:
    """Style context for GTK compatibility."""
    def add_class(self, *args):
        """Add a style class."""
        print(f"!!!{self=} add_class, {args=}")


class _Expandable:
    """Mixin for expandable controls."""
    def set_hexpand(self, value):
        """Set whether the control expands horizontally."""
        self._obj.HorizontalAlignment = HorizontalAlignment.Stretch if value else HorizontalAlignment.Left
        
    def set_vexpand(self, value):
        """Set whether the control expands vertically."""
        self._obj.VerticalAlignment = VerticalAlignment.Stretch if value else VerticalAlignment.Left


class _Tooltipped:
    """Mixin for controls that can have tooltips."""
    def set_tooltip_text(self, text):
        """Set the tooltip text of the control."""
        if text:
            tooltip = ToolTip()
            tooltip.Content = text
            ToolTipService.SetToolTip(self._obj, tooltip)