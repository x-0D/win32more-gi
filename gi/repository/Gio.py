"""
Gio compatibility layer for Windows.

This module provides Gio functionality for Windows applications.
"""

from gi.repository.__compat__ import _WinUIControl, _EventCtl

from win32more.Microsoft.UI.Xaml.Controls import (
    MenuFlyout, MenuFlyoutItem, MenuFlyoutSubItem
)

class Gio:
    """Gio compatibility layer."""
    
    class AppInfo:
        """Application information utilities."""
        @staticmethod
        def launch_default_for_uri(self, link):
            """Launch the default application for a URI."""
            print(f"!!![Gio.AppInfo] launch_default_for_uri, {link=}")
    
    class BusType:
        """D-Bus bus types."""
        SYSTEM = "SYSTEM"
    
    class DBusCallFlags:
        """D-Bus call flags."""
        NONE = "NONE"
    
    class DBusProxyFlags:
        """D-Bus proxy flags."""
        NONE = "NONE"
    
    class DBusProxy:
        """D-Bus proxy for remote object access."""
        @staticmethod
        def new_sync(bus, flags, *args):
            """Create a new D-Bus proxy synchronously."""
            print(f"!!![Gio.DBusProxy] new_sync, {bus=}, {flags=}, {args=}")
    
    class Menu(_WinUIControl):
        """Menu implementation."""
        def __init__(self):
            """Initialize a new menu."""
            self._obj = MenuFlyout()

        @staticmethod
        def new():
            """Create a new menu."""
            return Gio.Menu()

        def append_item(self, item):
            """Append an item to the menu."""
            self._obj.Items.Append(item._obj)

        def append_submenu(self, menu_name, submenu):
            """Append a submenu to the menu."""
            sub_item = MenuFlyoutSubItem()
            sub_item.Text = menu_name
            sub_item.Flyout = submenu._obj
            self._obj.Items.Append(sub_item)

    class MenuItem(_WinUIControl):
        """Menu item implementation."""
        def __init__(self, label, detailed_action=None):
            """Initialize a new menu item."""
            self._obj = MenuFlyoutItem()
            self._obj.Text = label
            if detailed_action:
                self._obj.Click += lambda sender, args: print(f"Activated {label} with action {detailed_action}")

        @staticmethod
        def new(label, detailed_action=None):
            """Create a new menu item."""
            return Gio.MenuItem(label, detailed_action)
    
    class Notification:
        """Notification implementation."""
        @staticmethod
        def new(title: str):
            """Create a new notification."""
            print(f"!!![Gio.Notification] new, {title=}")
    
    class SimpleAction(_EventCtl):
        """Simple action implementation."""
        def __init__(self, name, parameter_type=None, state=None):
            """Initialize a new simple action."""
            super().__init__()
            self.name = name
            self.parameter_type = parameter_type
            self.state = state
            self.enabled = True
            self._handlers = []

        @staticmethod
        def new(name, parameter_type=None, state=None):
            """Create a new simple action."""
            return Gio.SimpleAction(name, parameter_type, state)

        @staticmethod
        def new_stateful(name, parameter_type, state):
            """Create a new stateful simple action."""
            return Gio.SimpleAction(name, parameter_type, state)

        def set_enabled(self, enabled):
            """Set whether the action is enabled."""
            self.enabled = enabled

        def set_state(self, value):
            """Set the state of the action."""
            self.state = value
            self._emit_change_state(value)

        def set_state_hint(self, state_hint):
            """Set the state hint of the action."""
            pass  # Not directly supported in this implementation

        def _emit_activate(self, parameter):
            """Emit the activate signal."""
            for handler in self._handlers:
                handler(self, parameter)

        def _emit_change_state(self, value):
            """Emit the change-state signal."""
            for handler in self._handlers:
                handler(self, value)
    
    @staticmethod
    def bus_get_sync(bus_type, **kwargs):
        """Get a connection to a message bus."""
        print(f"!!!Gio bus_get_sync, {bus_type=}, {kwargs=}")