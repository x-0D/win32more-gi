"""
Gtk compatibility layer for Windows.

This module provides Gtk UI components for Windows applications.
"""

from enum import Enum
from ctypes import c_bool

from gi.repository.__compat__ import (
    _WinUIControl, _ItemSetter, _EventCtl, _TextField, 
    _Margin, _StyleContext, _Expandable, IReference
)
from gi.repository import DEBUG_COLORING

from win32more.Microsoft.UI.Xaml import (
    Visibility, HorizontalAlignment, VerticalAlignment, 
    RoutedEventArgs, Thickness
)
from win32more.Microsoft.UI.Xaml.Controls import (
    StackPanel, Button, TextBlock, Grid, Border, ProgressBar,
    ComboBox, ComboBoxItem, TextBox, ToolTip, ToolTipService
)
from win32more.Microsoft.UI.Xaml.Controls.Primitives import ToggleButton
from win32more.Microsoft.UI.Xaml.Media import SolidColorBrush
from win32more.Microsoft.UI import Colors
from win32more.Windows.Win32.System.WinRT import IInspectable

class Gtk:
    """Gtk compatibility layer."""
    
    class Adjustment:
        """Adjustment for ranges."""
        step_increment = 1
    
    class Orientation:
        """Widget orientation."""
        VERTICAL = 1
        HORIZONTAL = 0
    
    class Align(Enum):
        """Widget alignment."""
        END = 1
        CENTER = 2
        START = 0
    
    class Box(_WinUIControl, _Margin, _Expandable):
        """Box container implementation."""
        _orientation = None
        
        def __init__(self, orientation=None, spacing=None, halign=None, vexpand=True):
            """Initialize a new box."""
            self._obj = StackPanel()
            self._obj.HorizontalAlignment = HorizontalAlignment.Stretch
            self._obj.VerticalAlignment = VerticalAlignment.Stretch
            
            self._orientation = orientation if orientation is not None else Gtk.Orientation.VERTICAL
            self._obj.Orientation = 1 if self._orientation == Gtk.Orientation.VERTICAL else 0
            
            if spacing is not None:
                self._obj.Spacing = spacing
        
        def get_first_child(self):
            """Get the first child of the box."""
            print(f"!!!{self=} get_first_child")
            # Implementation needed
            if self._obj.Children.Size > 0:
                return self._obj.Children.GetAt(0)
            return None
        
        def append(self, child):
            """Append a child to the box."""
            try:
                print("[Box] Child is: ", child)
                winui_child = child.winui_get_obj()
                print("[Box] Appending: ", winui_child)
                self._obj.Children.Append(winui_child)
            except Exception as err:
                print(err)
        
        def remove(self, child):
            """Remove a child from the box."""
            try:
                winui_child = child.winui_get_obj()
                for i in range(self._obj.Children.Size):
                    if self._obj.Children.GetAt(i) == winui_child:
                        self._obj.Children.RemoveAt(i)
                        break
            except Exception as err:
                print(f"Error removing child: {err}")
        
        def prepend(self, child):
            """Prepend a child to the box."""
            try:
                print("[Box] Child is: ", child)
                winui_child = child.winui_get_obj()
                print("[Box] Prepending: ", winui_child)
                self._obj.Children.InsertAt(0, winui_child)
            except Exception as err:
                print(err)
    
    class Button(_WinUIControl, _ItemSetter, _EventCtl):
        """Button implementation."""
        _label = None
        
        def __init__(self, label: str = None, tooltip_text: str = None):
            """Initialize a new button."""
            super().__init__()
            self._obj = Button()
            self._obj.HorizontalAlignment = HorizontalAlignment.Stretch
            self._obj.VerticalAlignment = VerticalAlignment.Stretch

            def onClicked(x: IInspectable, y: RoutedEventArgs):
                self._event('clicked')
            
            self._obj.Click += onClicked

            if label is not None:
                self._label = TextBlock()
                self._label.Text = label
                self._label.HorizontalAlignment = HorizontalAlignment.Center
                self._obj.Content = self._label
            
            if tooltip_text is not None:
                toolTip = ToolTip()
                toolTip.Content = tooltip_text
                ToolTipService.SetToolTip(self._obj, toolTip)
        
        def set_icon_name(self, icon_name):
            """Set the icon name of the button."""
            self._icon = TextBlock()
            self._icon.Text = "img"  # Placeholder for icon
            self._icon.HorizontalAlignment = HorizontalAlignment.Left
            self._icon.VerticalAlignment = VerticalAlignment.Center
            panel = Grid()
            if self._label is not None:
                panel.Children.Append(self._label)
            panel.Children.Append(self._icon)
            self._obj.Content = panel
        
        def get_style_context(self):
            """Get the style context of the button."""
            return _StyleContext()
        
        def set_sensitive(self, value):
            """Set whether the button is sensitive."""
            self._obj.IsEnabled = value
        
        @staticmethod
        def new_from_icon_name(icon_name: str):
            """Create a new button with an icon."""
            button = Gtk.Button()
            button.set_icon_name(icon_name)
            return button
        
        def set_halign(self, value):
            """Set the horizontal alignment of the button."""
            if value == Gtk.Align.START:
                self._obj.HorizontalAlignment = HorizontalAlignment.Left
            elif value == Gtk.Align.CENTER:
                self._obj.HorizontalAlignment = HorizontalAlignment.Center
            elif value == Gtk.Align.END:
                self._obj.HorizontalAlignment = HorizontalAlignment.Right
        
        def set_valign(self, value):
            """Set the vertical alignment of the button."""
            if value == Gtk.Align.START:
                self._obj.VerticalAlignment = VerticalAlignment.Top
            elif value == Gtk.Align.CENTER:
                self._obj.VerticalAlignment = VerticalAlignment.Center
            elif value == Gtk.Align.END:
                self._obj.VerticalAlignment = VerticalAlignment.Bottom
    
    class ProgressBar(_WinUIControl):
        """Progress bar implementation."""
        def __init__(self):
            """Initialize a new progress bar."""
            self._obj = ProgressBar()
            self._obj.Height = 10
            self._obj.Minimum = 0
            self._obj.Maximum = 100

        @staticmethod
        def new():
            """Create a new progress bar."""
            return Gtk.ProgressBar()

        def set_fraction(self, fraction):
            """Set the fraction of the progress bar."""
            self._obj.Value = fraction * self._obj.Maximum

        def pulse(self):
            """Pulse the progress bar."""
            self._obj.IsIndeterminate = True

        def set_inverted(self, value):
            """Set whether the progress bar is inverted."""
            # Not directly supported in WinUI 3
            print(f"!!!{self=} set_inverted, {value=}")

        def set_text(self, text):
            """Set the text of the progress bar."""
            # Not directly supported in WinUI 3
            print(f"!!!{self=} set_text, {text=}")

        def set_show_text(self, show_text):
            """Set whether to show text on the progress bar."""
            # Not directly supported in WinUI 3
            print(f"!!!{self=} set_show_text, {show_text=}")
    
    class ToggleButton(_WinUIControl, _ItemSetter, _EventCtl):
        """Toggle button implementation."""
        _isChecked: IReference[c_bool]
        
        def __init__(self, label: str = None, tooltip_text: str = None):
            """Initialize a new toggle button."""
            super().__init__()
            self._obj = ToggleButton()

            self._obj.Background = SolidColorBrush(Colors.Transparent)
            self._obj.BorderThickness = Thickness(1, 1, 1, 1)
            self._obj.BorderBrush = SolidColorBrush(Colors.Transparent)
            self._obj.HorizontalAlignment = HorizontalAlignment.Stretch
            
            if label is not None:
                self._label = TextBlock()
                self._label.Text = label
                self._label.HorizontalAlignment = HorizontalAlignment.Center
                self._label.VerticalAlignment = VerticalAlignment.Center
                self._obj.Content = self._label
            
            if tooltip_text is not None:
                toolTip = ToolTip()
                toolTip.Content = tooltip_text
                ToolTipService.SetToolTip(self._obj, toolTip)
            
            def onChecked(x: IInspectable, y: RoutedEventArgs):
                isChecked = x.as_(ToggleButton).IsChecked
                print(f"{x=} {isChecked=}")
                if isChecked:
                    self._event('clicked')
            
            self._obj.Checked += onChecked
        
        def set_icon_name(self, icon_name):
            """Set the icon name of the toggle button."""
            # Not fully implemented - would need icon loading logic
            print(f"!!!{self=} set_icon_name, {icon_name=}")
        
        def get_style_context(self):
            """Get the style context of the toggle button."""
            return _StyleContext()
        
        def set_sensitive(self, value):
            """Set whether the toggle button is sensitive."""
            self._obj.IsEnabled = value
        
        def set_active(self, value: bool):
            """Set whether the toggle button is active."""
            self._obj.IsChecked = value
        
        @staticmethod
        def new_from_icon_name(icon_name: str):
            """Create a new toggle button with an icon."""
            toggle = Gtk.ToggleButton()
            toggle.set_icon_name(icon_name)
            return toggle
    
    class ComboBoxText(_WinUIControl, _TextField, _EventCtl):
        """Combo box text implementation."""
        def __init__(self):
            """Initialize a new combo box text."""
            super().__init__()
            self._obj = TextBox()
            
            def onTextChanged(x: IInspectable, y: RoutedEventArgs):
                self._event('changed')
            
            self._obj.TextChanged += onTextChanged
            
        def append_text(self, text):
            """Append text to the combo box."""
            # Not directly supported in TextBox - would need custom implementation
            print(f"!!!{self=} append_text, {text=}")
            
        def get_active_text(self):
            """Get the active text of the combo box."""
            return self._obj.Text
            
        def set_active(self, index):
            """Set the active item of the combo box."""
            # Not directly supported in TextBox - would need custom implementation
            print(f"!!!{self=} set_active, {index=}")
    
    class DropDown(_WinUIControl, _EventCtl):
        """Drop-down implementation."""
        def __init__(self, model=None):
            """Initialize a new drop-down."""
            super().__init__()
            self._obj = ComboBox()
            self._obj.SelectionChanged += self.on_selection_changed
            
            if model:
                self.set_model(model)

        @staticmethod
        def new(model=None):
            """Create a new drop-down."""
            return Gtk.DropDown(model)

        @staticmethod
        def new_from_strings(strings):
            """Create a new drop-down from strings."""
            drop_down = Gtk.DropDown()
            for string in strings:
                item = ComboBoxItem()
                item.Content = string
                drop_down._obj.Items.Append(item)
            return drop_down

        def set_model(self, model):
            """Set the model of the drop-down."""
            self._obj.Items.Clear()
            for item in model:
                combo_item = ComboBoxItem()
                combo_item.Content = item
                self._obj.Items.Append(combo_item)

        def get_selected(self):
            """Get the selected index of the drop-down."""
            selected_index = self._obj.SelectedIndex
            return selected_index if selected_index != -1 else None

        def get_selected_item(self):
            """Get the selected item of the drop-down."""
            selected_item = self._obj.SelectedItem
            return selected_item.Content if selected_item else None

        def set_enable_search(self, enable_search):
            """Set whether search is enabled in the drop-down."""
            # Not directly supported in WinUI 3
            pass

        def set_expression(self, expression):
            """Set the expression of the drop-down."""
            # Not directly supported in WinUI 3
            pass

        def set_factory(self, factory):
            """Set the factory of the drop-down."""
            # Not directly supported in WinUI 3
            pass

        def set_header_factory(self, header_factory):
            """Set the header factory of the drop-down."""
            # Not directly supported in WinUI 3
            pass

        def set_list_factory(self, list_factory):
            """Set the list factory of the drop-down."""
            # Not directly supported in WinUI 3
            pass

        def set_search_match_mode(self, search_match_mode):
            """Set the search match mode of the drop-down."""
            # Not directly supported in WinUI 3
            pass

        def set_selected(self, index):
            """Set the selected index of the drop-down."""
            if index is not None and index >= 0 and index < self._obj.Items.Size:
                self._obj.SelectedIndex = index

        def set_show_arrow(self, show_arrow):
            """Set whether to show an arrow in the drop-down."""
            # Not applicable in WinUI 3
            pass

        def on_selection_changed(self, sender, args):
            """Handle selection change event."""
            selected_item = self.get_selected_item()
            print(f"Selected: {selected_item}")
            self._event('changed')
    
    class Entry(_WinUIControl, _TextField, _EventCtl):
        """Entry implementation."""
        def __init__(self):
            """Initialize a new entry."""
            super().__init__()
            self._obj = TextBox()
            
            def onTextChanged(x: IInspectable, y: RoutedEventArgs):
                self._event('changed')
            
            self._obj.TextChanged += onTextChanged
            
        def set_input_purpose(self, purpose):
            """Set the input purpose of the entry."""
            if purpose == Gtk.InputPurpose.NUMBER:
                # Set input scope to number
                pass
    
    class FileDialog:
        """File dialog implementation."""
        def __init__(self):
            """Initialize a new file dialog."""
            pass
            
        def select_folder(self, title=None, parent=None, callback=None):
            """Select a folder."""
            # Would need to implement Windows folder picker
            print(f"!!!{self=} select_folder, title={title}, parent={parent}")
            if callback:
                # Mock implementation - would return a folder path in real implementation
                callback(self, True, "/mock/folder/path")
    
    class Frame(_WinUIControl, _ItemSetter, _Margin):
        """Frame implementation."""
        def __init__(self):
            """Initialize a new frame."""
            self._obj = Border()
            if DEBUG_COLORING:
                self._obj.Background = SolidColorBrush(Colors.DarkOrchid)
            self._obj.HorizontalAlignment = HorizontalAlignment.Stretch
            self._obj.VerticalAlignment = VerticalAlignment.Stretch
            
        def set_label(self, label):
            """Set the label of the frame."""
            # Not directly supported in Border - would need custom implementation
            print(f"!!!{self=} set_label, {label=}")
    
    class IconTheme:
        """Icon theme implementation."""
        @staticmethod
        def get_for_display(*args):
            """Get the icon theme for a display."""
            return Gtk.IconTheme()
        
        def add_search_path(self, path):
            """Add a search path to the icon theme."""
            print(f"!!!{self=} add_search_path, {path=}")
    
    class Image(_WinUIControl):
        """Image implementation."""
        def __init__(self):
            """Initialize a new image."""
            self._obj = TextBlock()
            self._obj.Text = "img"
            self._obj.HorizontalAlignment = HorizontalAlignment.Left
            self._obj.VerticalAlignment = VerticalAlignment.Center

        def set_from_icon_name(self, icon_name, size=None):
            """Set the image from an icon name."""
            # Would need icon loading logic
            print(f"!!!{self=} set_from_icon_name, {icon_name=}, {size=}")

        @staticmethod
        def new():
            """Create a new image."""
            return Gtk.Image()

        @staticmethod
        def new_from_icon_name(icon_name, size=None):
            """Create a new image from an icon name."""
            image = Gtk.Image()
            image.set_from_icon_name(icon_name, size)
            return image
    
    class InputPurpose:
        """Input purpose constants."""
        NUMBER = "NUMBER"
    
    class Label(_WinUIControl, _TextField):
        """Label implementation."""
        def __init__(self, label=None):
            """Initialize a new label."""
            self._obj = TextBlock()
            self._obj.Text = label
            self._obj.HorizontalAlignment = HorizontalAlignment.Center
            self._obj.VerticalAlignment = VerticalAlignment.Center
        
        def get_style_context(self):
            """Get the style context of the label."""
            return _StyleContext()
        
        def set_ellipsize(self, mode):
            """Set the ellipsize mode of the label."""
            # Not directly supported in TextBlock
            print(f"!!!{self=} set_ellipsize, {mode=}")
        
        def set_halign(self, value):
            """Set the horizontal alignment of the label."""
            if value == Gtk.Align.START:
                self._obj.HorizontalAlignment = HorizontalAlignment.Left
            elif value == Gtk.Align.CENTER:
                self._obj.HorizontalAlignment = HorizontalAlignment.Center
            elif value == Gtk.Align.END:
                self._obj.HorizontalAlignment = HorizontalAlignment.Right
        
        def set_valign(self, value):
            """Set the vertical alignment of the label."""
            if value == Gtk.Align.START:
                self._obj.VerticalAlignment = VerticalAlignment.Top
            elif value == Gtk.Align.CENTER:
                self._obj.VerticalAlignment = VerticalAlignment.Center
            elif value == Gtk.Align.END:
                self._obj.VerticalAlignment = VerticalAlignment.Bottom
    
    class License:
        """License constants."""
        MPL_2_0 = "MPL_2_0"
    
    class MenuButton(_WinUIControl, _EventCtl):
        """Menu button implementation."""
        _label = None
        
        def __init__(self, label: str = None, tooltip_text: str = None):
            """Initialize a new menu button."""
            super().__init__()
            from win32more.Microsoft.UI.Xaml.Controls import DropDownButton
            
            self._obj = DropDownButton()
            self._obj.HorizontalAlignment = HorizontalAlignment.Stretch
            self._obj.VerticalAlignment = VerticalAlignment.Stretch
            
            if label is not None:
                self._label = TextBlock()
                self._label.Text = label
                self._label.HorizontalAlignment = HorizontalAlignment.Center
                self._label.VerticalAlignment = VerticalAlignment.Center
                self._obj.Content = self._label
            
            if tooltip_text is not None:
                toolTip = ToolTip()
                toolTip.Content = tooltip_text
                ToolTipService.SetToolTip(self._obj, toolTip)
        
        def set_icon_name(self, icon_name):
            """Set the icon name of the menu button."""
            self._icon = TextBlock()
            self._icon.Text = "img"  # Placeholder for icon
            self._icon.HorizontalAlignment = HorizontalAlignment.Left
            self._icon.VerticalAlignment = VerticalAlignment.Center
            panel = Grid()
            if self._label is not None:
                panel.Children.Append(self._label)
            panel.Children.Append(self._icon)
            self._obj.Content = panel
        
        def set_menu_model(self, menu):
            """Set the menu model of the menu button."""
            self._obj.Flyout = menu.winui_get_obj()
    
    class ScrolledWindow(_WinUIControl, _ItemSetter):
        """Scrolled window implementation."""
        def __init__(self):
            """Initialize a new scrolled window."""
            from win32more.Microsoft.UI.Xaml.Controls import ScrollViewer
            
            self._obj = ScrollViewer()
            if DEBUG_COLORING:
                self._obj.Background = SolidColorBrush(Colors.DarkOrange)
            self._obj.HorizontalAlignment = HorizontalAlignment.Stretch
            self._obj.VerticalAlignment = VerticalAlignment.Stretch
            
        def set_policy(self, hscrollbar_policy, vscrollbar_policy):
            """Set the scrollbar policy of the scrolled window."""
            # Map GTK policies to WinUI ScrollMode
            # GTK_POLICY_ALWAYS, GTK_POLICY_AUTOMATIC, GTK_POLICY_NEVER
            print(f"!!!{self=} set_policy, {hscrollbar_policy=}, {vscrollbar_policy=}")
    
    class Separator(_WinUIControl):
        """Separator implementation."""
        def __init__(self, margin_top=0, margin_bottom=0):
            """Initialize a new separator."""
            self._obj = Grid()
            if DEBUG_COLORING:
                self._obj.Background = SolidColorBrush(Colors.DarkOrange)
            self._obj.Height = 2
            self._obj.HorizontalAlignment = HorizontalAlignment.Stretch
            self._obj.VerticalAlignment = VerticalAlignment.Stretch
            
            # Apply margins
            margin = Thickness()
            margin.Top = margin_top
            margin.Bottom = margin_bottom
            self._obj.Margin = margin
    
    class Settings:
        """Settings implementation."""
        _instance = None
        
        @staticmethod
        def get_default():
            """Get the default settings."""
            if Gtk.Settings._instance is None:
                Gtk.Settings._instance = Gtk.Settings()
            return Gtk.Settings._instance
        
        def set_property(self, key, value):
            """Set a property of the settings."""
            print(f"!!!{self=} set_property, {key=}, {value=}")
    
    class Widget:
        """Widget utilities."""
        @staticmethod
        def set_hexpand(widget, expand: bool):
            """Set whether a widget expands horizontally."""
            if hasattr(widget, 'set_hexpand'):
                widget.set_hexpand(expand)
            else:
                print(f"!!!Widget.set_hexpand, {widget=} does not support set_hexpand")
                
        @staticmethod
        def set_vexpand(widget, expand: bool):
            """Set whether a widget expands vertically."""
            if hasattr(widget, 'set_vexpand'):
                widget.set_vexpand(expand)
            else:
                print(f"!!!Widget.set_vexpand, {widget=} does not support set_vexpand")