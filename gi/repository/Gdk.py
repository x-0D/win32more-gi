"""
Gdk compatibility layer for Windows.

This module provides Gdk (GIMP Drawing Kit) functionality for Windows applications.
"""

class Gdk:
    """Gdk compatibility layer."""
    
    class Display:
        """Display implementation."""
        @staticmethod
        def get_default():
            """Get the default display."""
            print(f"!!![Gdk.Display] get_default")
            return Gdk.Display()
            
        def get_monitor(self, monitor_num):
            """Get a monitor by number."""
            print(f"!!![Gdk.Display] get_monitor, {monitor_num=}")
            return Gdk.Monitor()
            
        def get_primary_monitor(self):
            """Get the primary monitor."""
            print(f"!!![Gdk.Display] get_primary_monitor")
            return Gdk.Monitor()
            
    class Monitor:
        """Monitor implementation."""
        def get_geometry(self):
            """Get the geometry of the monitor."""
            print(f"!!![Gdk.Monitor] get_geometry")
            return Gdk.Rectangle()
            
        def get_scale_factor(self):
            """Get the scale factor of the monitor."""
            print(f"!!![Gdk.Monitor] get_scale_factor")
            return 1
            
    class Rectangle:
        """Rectangle implementation."""
        def __init__(self):
            """Initialize a new rectangle."""
            self.x = 0
            self.y = 0
            self.width = 1920  # Default width
            self.height = 1080  # Default height