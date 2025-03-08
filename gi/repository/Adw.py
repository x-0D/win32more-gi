"""
Adw compatibility layer for Windows.

This module provides Adwaita (libadwaita) UI components for Windows applications.
"""

import asyncio

from gi.repository.__compat__ import (
    _WinUIControl, _ItemSetter, _EventCtl, _Expandable
)
from gi.repository import DEBUG_COLORING

from win32more.Microsoft.UI.Xaml import (
    Visibility, HorizontalAlignment, VerticalAlignment, 
    RoutedEventArgs, Thickness, CornerRadius, Window, GridLength, GridUnitType
)
from win32more.Microsoft.UI.Xaml.Controls import (
    StackPanel, TextBlock, Grid, Border, ProgressRing, ContentDialog,
    SplitView, SplitViewDisplayMode
)
from win32more.Microsoft.UI.Xaml.Media import MicaBackdrop, SolidColorBrush
from win32more.Microsoft.UI import Colors
from win32more.xaml import XamlApplication
from win32more.Windows.Win32.System.WinRT import IInspectable

class Adw:
    """Adw compatibility layer for libadwaita components."""
    
    class AlertDialog(_WinUIControl, _ItemSetter):
        """Alert dialog implementation."""
        def __init__(self):
            """Initialize a new alert dialog."""
            self._obj = ContentDialog()
            self._obj.Content = "Check connection and try again."
            self._obj.CloseButtonText = "Ok"

        def present(self, window):
            """Present the alert dialog."""
            self._obj.XamlRoot = window.winui_get_obj().XamlRoot
            async def wrapasync():
                await self._obj.ShowAsync()
            loop = asyncio.get_event_loop()
            loop.create_task(wrapasync())
            
        def force_close(self):
            """Force close the alert dialog."""
            self._obj.Hide()
            
        def set_can_close(self, value):
            """Set whether the alert dialog can be closed."""
            # Not directly supported in ContentDialog
            print(f"!!!{self=} set_can_close, {value=}")
            
        def set_heading(self, heading):
            """Set the heading of the alert dialog."""
            self._obj.Title = heading
            
        def set_body(self, body):
            """Set the body of the alert dialog."""
            self._obj.Content = body
            
        def add_response(self, id, label):
            """Add a response button to the alert dialog."""
            if id == "ok":
                self._obj.PrimaryButtonText = label
            elif id == "cancel":
                self._obj.CloseButtonText = label
            elif id == "other":
                self._obj.SecondaryButtonText = label
    
    class Application(_EventCtl):
        """Application implementation."""
        _XamlApplication: XamlApplication
        
        def __init__(self, application_id=None, flags=None):
            """Initialize a new application."""
            super().__init__()
            app_self = self
            self.application_id = application_id
            
            class InternalAppWrapper(XamlApplication):
                def OnLaunched(self, args):
                    app_self._event('activate')
                    
            self._XamlApplication = InternalAppWrapper

        def run(self, *args):
            """Run the application."""
            XamlApplication.Start(self._XamlApplication)
            
        def quit(self):
            """Quit the application."""
            # Would need to implement application shutdown
            print(f"!!!{self=} quit")
            
        def add_action(self, action):
            """Add an action to the application."""
            # Would need to implement action handling
            print(f"!!!{self=} add_action, {action=}")
            
        def add_main_option(self, long_name, short_name, flags, arg, description, arg_description):
            """Add a main option to the application."""
            # Would need to implement command line option handling
            print(f"!!!{self=} add_main_option, {long_name=}")
    
    class ApplicationWindow(_WinUIControl, _EventCtl):
        """Application window implementation."""
        _window: Window
        
        def _window_SetTitleBar(self, widget):
            """Set the title bar of the window."""
            print("Setting HeaderBar: ", widget)
            self._header_bar = widget
            self._window.SetTitleBar = widget.winui_get_obj()
            
        def _window_GetTitleBar(self):
            """Get the title bar of the window."""
            print("Getting HeaderBar")
            return self._header_bar
            
        header_bar = property(_window_GetTitleBar, _window_SetTitleBar)

        def __init__(self, application=None):
            """Initialize a new application window."""
            super().__init__()
            self._destroying = False
            self._window = Window()
            self._window.ExtendsContentIntoTitleBar = True
            self._window.SystemBackdrop = MicaBackdrop()
            self._obj = Grid()
            
            if DEBUG_COLORING:
                self._obj.Background = SolidColorBrush(Colors.Indigo)
                
            self._obj.HorizontalAlignment = HorizontalAlignment.Stretch
            self._obj.VerticalAlignment = VerticalAlignment.Stretch

            column1 = ColumnDefinition()
            column1.Width = GridLength(1, GridUnitType.Star)
            self._obj.ColumnDefinitions.Append(column1)

            self._window.Content = self._obj
            self.application = application

        def present(self):
            """Present the application window."""
            def on_close(x, y):
                y.Cancel = not self._destroying
                self._event('close-request')
                
            self._window.Closed += on_close
            self._window.Activate()

        def destroy(self):
            """Destroy the application window."""
            self._destroying = True
            self._window.Close()
            
        def set_title(self, title):
            """Set the title of the application window."""
            self._window.Title = title

        def set_default_size(self, width: int, height: int):
            """Set the default size of the application window."""
            self._window.Width = width
            self._window.Height = height
            
        def set_size_request(self, width: int, height: int):
            """Set the size request of the application window."""
            self._window.MinWidth = width
            self._window.MinHeight = height
            
        def set_content(self, content):
            """Set the content of the application window."""
            print("[AppWindow] Content is: ", content)
            print("[AppWindow] Setting Content:", content.winui_get_obj())
            Grid.SetRow(content.winui_get_obj(), 0)
            self._obj.Children.Append(content.winui_get_obj())
            
        def is_visible(self) -> bool:
            """Check if the application window is visible."""
            return self._window.Visible
            
        def set_visible(self, visibility: bool):
            """Set the visibility of the application window."""
            if visibility:
                self._window.Activate()
            else:
                self._window.Hide()
    
    class HeaderBar(_WinUIControl):
        """Header bar implementation."""
        def __init__(self):
            """Initialize a new header bar."""
            # Create a custom title bar grid
            self._obj = Grid()
            
            if DEBUG_COLORING:
                self._obj.Background = SolidColorBrush(Colors.DarkMagenta)
                
            self._obj.HorizontalAlignment = HorizontalAlignment.Stretch
            self._obj.VerticalAlignment = VerticalAlignment.Stretch

            self._obj.Height = 48  # Follow title bar design guidance
            
            column1 = ColumnDefinition()
            column1.Width = GridLength(1, GridUnitType.Star)
            column2 = ColumnDefinition()
            column2.Width = GridLength(4, GridUnitType.Star)
            column3 = ColumnDefinition()
            column3.Width = GridLength(1, GridUnitType.Star)
            
            self._obj.ColumnDefinitions.Append(column1)
            self._obj.ColumnDefinitions.Append(column2)
            self._obj.ColumnDefinitions.Append(column3)
            
            placeholder1 = Grid()
            if DEBUG_COLORING:
                placeholder1.Background = SolidColorBrush(Colors.DarkViolet)
            placeholder1.HorizontalAlignment = HorizontalAlignment.Stretch
            Grid.SetColumn(placeholder1, 0)
            
            placeholder2 = Grid()
            if DEBUG_COLORING:
                placeholder2.Background = SolidColorBrush(Colors.DarkBlue)
            placeholder2.HorizontalAlignment = HorizontalAlignment.Stretch
            Grid.SetColumn(placeholder2, 1)
            
            placeholder3 = Grid()
            if DEBUG_COLORING:
                placeholder3.Background = SolidColorBrush(Colors.DarkOliveGreen)
            placeholder3.HorizontalAlignment = HorizontalAlignment.Stretch
            Grid.SetColumn(placeholder3, 2)

            self._obj.Children.Append(placeholder1)
            self._obj.Children.Append(placeholder2)
            self._obj.Children.Append(placeholder3)

        def pack_start(self, child):
            """Pack a child at the start of the header bar."""
            Grid.SetColumn(child.winui_get_obj(), 0)
            self._obj.Children.Append(child.winui_get_obj())
            
        def pack_end(self, child):
            """Pack a child at the end of the header bar."""
            Grid.SetColumn(child.winui_get_obj(), 2)
            self._obj.Children.Append(child.winui_get_obj())
            
        def get_style_context(self):
            """Get the style context of the header bar."""
            return _StyleContext()
            
        def set_title_widget(self, widget):
            """Set the title widget of the header bar."""
            Grid.SetColumn(widget.winui_get_obj(), 1)
            self._obj.Children.Append(widget.winui_get_obj())
            
        def set_show_title_buttons(self, show):
            """Set whether to show title buttons."""
            # Not directly supported - would need custom implementation
            print(f"!!!{self=} set_show_title_buttons, {show=}")
    
    class Spinner(_WinUIControl):
        """Spinner implementation."""
        def __init__(self):
            """Initialize a new spinner."""
            self._obj = ProgressRing()
            self._obj.IsActive = True  # Set the spinner to be active by default
            self._obj.Visibility = Visibility.Visible  # Ensure the spinner is visible

        @staticmethod
        def new():
            """Create a new spinner."""
            return Adw.Spinner()

        def set_size_request(self, width, height):
            """Set the size request of the spinner."""
            self._obj.Width = width
            self._obj.Height = height

        def set_active(self, active):
            """Set whether the spinner is active."""
            self._obj.IsActive = active

        def set_visibility(self, visible):
            """Set the visibility of the spinner."""
            self._obj.Visibility = Visibility.Visible if visible else Visibility.Collapsed

    class AboutDialog(_WinUIControl):
        """About dialog implementation."""
        def __init__(self):
            """Initialize a new about dialog."""
            self._obj = ContentDialog()
            self._obj.Title = "About"
            self._obj.CloseButtonText = "Close"
            
            # Create content layout
            content = StackPanel()
            content.Orientation = 1  # Vertical
            self._obj.Content = content
            
        def set_application_name(self, name):
            """Set the application name of the about dialog."""
            app_name = TextBlock()
            app_name.Text = name
            app_name.FontSize = 24
            content = self._obj.Content
            content.Children.Append(app_name)
            
        def set_version(self, version):
            """Set the version of the about dialog."""
            version_text = TextBlock()
            version_text.Text = f"Version: {version}"
            content = self._obj.Content
            content.Children.Append(version_text)
            
        def set_comments(self, comments):
            """Set the comments of the about dialog."""
            comments_text = TextBlock()
            comments_text.Text = comments
            content = self._obj.Content
            content.Children.Append(comments_text)
            
        def set_website(self, website):
            """Set the website of the about dialog."""
            website_text = TextBlock()
            website_text.Text = website
            content = self._obj.Content
            content.Children.Append(website_text)
            
        def set_developers(self, developers):
            """Set the developers of the about dialog."""
            devs_text = TextBlock()
            devs_text.Text = "Developers:\n" + "\n".join(developers)
            content = self._obj.Content
            content.Children.Append(devs_text)
            
        def set_license_type(self, license_type):
            """Set the license type of the about dialog."""
            license_text = TextBlock()
            license_text.Text = f"License: {license_type}"
            content = self._obj.Content
            content.Children.Append(license_text)
            
        def present(self, parent):
            """Present the about dialog."""
            self._obj.XamlRoot = parent.winui_get_obj().XamlRoot
            async def wrapasync():
                await self._obj.ShowAsync()
            loop = asyncio.get_event_loop()
            loop.create_task(wrapasync())

    class Banner(_WinUIControl):
        """Banner implementation."""
        def __init__(self, title=None):
            """Initialize a new banner."""
            self._obj = Grid()
            self._obj.Height = 48
            self._obj.HorizontalAlignment = HorizontalAlignment.Stretch
            
            # Create banner content
            self._content = StackPanel()
            self._content.Orientation = 0  # Horizontal
            self._obj.Children.Append(self._content)
            
            if title:
                title_text = TextBlock()
                title_text.Text = title
                self._content.Children.Append(title_text)
                
        def set_title(self, title):
            """Set the title of the banner."""
            # Find or create title text block
            title_text = None
            for i in range(self._content.Children.Size):
                child = self._content.Children.GetAt(i)
                if isinstance(child, TextBlock):
                    title_text = child
                    break
                    
            if not title_text:
                title_text = TextBlock()
                self._content.Children.Append(title_text)
                
            title_text.Text = title
            
        def set_button_label(self, label):
            """Set the button label of the banner."""
            # Find or create button
            button = None
            from win32more.Microsoft.UI.Xaml.Controls import Button
            
            for i in range(self._content.Children.Size):
                child = self._content.Children.GetAt(i)
                if isinstance(child, Button):
                    button = child
                    break
                    
            if not button:
                button = Button()
                self._content.Children.Append(button)
                
            button.Content = label
            
        def set_revealed(self, revealed):
            """Set whether the banner is revealed."""
            self._obj.Visibility = Visibility.Visible if revealed else Visibility.Collapsed

    class Bin(_WinUIControl, _ItemSetter):
        """Bin implementation."""
        def __init__(self):
            """Initialize a new bin."""
            self._obj = Border()
            self._obj.CornerRadius = CornerRadius(TopLeft=5, TopRight=5, BottomRight=5, BottomLeft=5)
            self._obj.Padding = Thickness(Left=10, Top=10, Right=10, Bottom=10)

        @staticmethod
        def new():
            """Create a new bin."""
            return Adw.Bin()

        def get_style_context(self):
            """Get the style context of the bin."""
            return _StyleContext()

        def set_background(self, color):
            """Set the background of the bin."""
            self._obj.Background = SolidColorBrush(color)

        def set_cornerRadius(self, radius):
            """Set the corner radius of the bin."""
            self._obj.CornerRadius = CornerRadius(TopLeft=radius, TopRight=radius, BottomRight=radius, BottomLeft=radius)

        def set_padding(self, padding):
            """Set the padding of the bin."""
            self._obj.Padding = Thickness(Left=padding, Top=padding, Right=padding, Bottom=padding)

    class ButtonContent(_WinUIControl):
        """Button content implementation."""
        def __init__(self):
            """Initialize new button content."""
            self._obj = Grid()
            self._obj.HorizontalAlignment = HorizontalAlignment.Stretch
            self._obj.VerticalAlignment = VerticalAlignment.Stretch

            row1 = RowDefinition()
            row1.Height = GridLength(1, GridUnitType.Star)
            row2 = RowDefinition()
            row2.Height = GridLength(3, GridUnitType.Star)
            self._obj.RowDefinitions.Append(row1)
            self._obj.RowDefinitions.Append(row2)

        def set_label(self, label):
            """Set the label of the button content."""
            text = TextBlock()
            text.Text = label
            text.HorizontalAlignment = HorizontalAlignment.Center
            text.VerticalAlignment = VerticalAlignment.Center
            Grid.SetRow(text, 1)
            self._obj.Children.Append(text)
            
        def set_icon_name(self, name):
            """Set the icon name of the button content."""
            # Would need icon loading logic
            print(f"!!!{self=} set_icon_name, {name=}")
    
    class OverlaySplitView(_WinUIControl):
        """Overlay split view implementation."""
        def __init__(self):
            """Initialize a new overlay split view."""
            self._obj = SplitView()
            
            if DEBUG_COLORING:
                self._obj.Background = SolidColorBrush(Colors.Red)
                
            self._obj.HorizontalAlignment = HorizontalAlignment.Stretch
            self._obj.VerticalAlignment = VerticalAlignment.Stretch
            self._obj.DisplayMode = SplitViewDisplayMode.Inline
            self._obj.IsPaneOpen = True

        @staticmethod
        def new():
            """Create a new overlay split view."""
            return Adw.OverlaySplitView()

        def set_sidebar(self, content):
            """Set the sidebar of the overlay split view."""
            self._obj.Pane = content.winui_get_obj()

        def set_content(self, content):
            """Set the content of the overlay split view."""
            self._obj.Content = content.winui_get_obj()
            
        def set_show_sidebar(self, show):
            """Set whether to show the sidebar."""
            self._obj.IsPaneOpen = show
            
        def get_show_sidebar(self):
            """Get whether the sidebar is shown."""
            return self._obj.IsPaneOpen
            
        def set_sidebar_width_fraction(self, fraction):
            """Set the sidebar width fraction."""
            # Convert fraction to actual width
            self._obj.OpenPaneLength = 250 * fraction  # Assuming 250 is the default width

    class ActionRow(_WinUIControl):
        """Action row implementation."""
        def __init__(self, title: str = None, subtitle: str = None, icon_name: str = None):
            """Initialize a new action row."""
            self._obj = StackPanel()
            self._obj.Orientation = 0  # Horizontal
            self._content_stack = StackPanel()
            self._content_stack.Orientation = 1  # Vertical
            self._obj.Children.Append(self._content_stack)

            self._title_text = TextBlock()
            self._title_text.Text = title
            self._title_text.FontSize = 18
            self._content_stack.Children.Append(self._title_text)

            self._subtitle_text = TextBlock()
            self._subtitle_text.Text = subtitle
            self._subtitle_text.FontSize = 14
            self._content_stack.Children.Append(self._subtitle_text)

            # Add activatable widget (e.g., a button or checkbox)
            self._activatable_widget = None

        def set_title(self, title):
            """Set the title of the action row."""
            self._title_text.Text = title

        def set_subtitle(self, subtitle):
            """Set the subtitle of the action row."""
            self._subtitle_text.Text = subtitle

        def add_prefix(self, widget):
            """Add a prefix widget to the action row."""
            self._obj.Children.InsertAt(0, widget.winui_get_obj())

        def add_suffix(self, widget):
            """Add a suffix widget to the action row."""
            self._obj.Children.Append(widget.winui_get_obj())

        def set_activatable_widget(self, widget):
            """Set the activatable widget of the action row."""
            self._activatable_widget = widget
            # Make the row activatable if a widget is provided
            if widget:
                self._obj.Tapped += lambda sender, args: widget.winui_get_obj().Invoke()

        def set_icon_name(self, icon_name: str):
            """Set the icon name of the action row."""
            # Would need icon loading logic
            pass

        def set_subtitle_lines(self, lines: int):
            """Set the number of subtitle lines of the action row."""
            # Not directly supported in TextBlock
            pass

        def set_subtitle_selectable(self, selectable: bool):
            """Set whether the subtitle of the action row is selectable."""
            # Not directly supported in TextBlock
            pass

    class PasswordEntryRow(_WinUIControl):
        """Password entry row implementation."""
        def __init__(self, title=None):
            """Initialize a new password entry row."""
            self._obj = StackPanel()
            self._obj.Orientation = 0  # Horizontal
            
            # Title
            if title:
                title_text = TextBlock()
                title_text.Text = title
                title_text.VerticalAlignment = VerticalAlignment.Center
                self._obj.Children.Append(title_text)
                
            # Password entry
            from win32more.Microsoft.UI.Xaml.Controls import PasswordBox
            self._password_box = PasswordBox()
            self._password_box.Width = 200
            self._obj.Children.Append(self._password_box)
            
        def get_text(self):
            """Get the text of the password entry."""
            return self._password_box.Password
            
        def set_text(self, text):
            """Set the text of the password entry."""
            self._password_box.Password = text
            
        def set_show_apply_button(self, show):
            """Set whether to show the apply button."""
            # Not directly supported - would need custom implementation
            pass

    class PreferencesDialog(_WinUIControl):
        """Preferences dialog implementation."""
        def __init__(self, title: str):
            """Initialize a new preferences dialog."""
            self._obj = ContentDialog()
            self._obj.Title = title
            self._obj.PrimaryButtonText = "Apply"
            self._obj.CloseButtonText = "Cancel"
            self._content = StackPanel()
            self._content.Orientation = 1  # Vertical
            self._obj.Content = self._content
            self._search_enabled = False
            self._search_box = None

        def set_search_enabled(self, enabled: bool):
            """Set whether search is enabled in the preferences dialog."""
            self._search_enabled = enabled
            if enabled:
                self._add_search_box()
            else:
                self._remove_search_box()

        def _add_search_box(self):
            """Add a search box to the preferences dialog."""
            if not self._search_box:
                from win32more.Microsoft.UI.Xaml.Controls import TextBox
                self._search_box = TextBox()
                self._search_box.PlaceholderText = "Search"
                self._content.Children.InsertAt(0, self._search_box)

        def _remove_search_box(self):
            """Remove the search box from the preferences dialog."""
            if self._search_box:
                self._content.Children.Remove(self._search_box)
                self._search_box = None

        def add(self, page):
            """Add a page to the preferences dialog."""
            self._content.Children.Append(page._obj)
            
        def present(self, parent):
            """Present the preferences dialog."""
            self._obj.XamlRoot = parent.winui_get_obj().XamlRoot
            async def wrapasync():
                await self._obj.ShowAsync()
            loop = asyncio.get_event_loop()
            loop.create_task(wrapasync())

    class PreferencesGroup(_WinUIControl):
        """Preferences group implementation."""
        def __init__(self, title: str = None):
            """Initialize a new preferences group."""
            self._obj = StackPanel()
            self._obj.Orientation = 1  # Vertical
            
            # Add header
            header = TextBlock()
            header.Text = title
            header.FontSize = 24
            header.Margin = Thickness(Left=10, Top=10, Right=10, Bottom=10)
            self._obj.Children.Append(header)

        def add(self, preference):
            """Add a preference to the preferences group."""
            self._obj.Children.Append(preference._obj)
            
        def set_title(self, title):
            """Set the title of the preferences group."""
            for i in range(self._obj.Children.Size):
                child = self._obj.Children.GetAt(i)
                if isinstance(child, TextBlock) and child.FontSize == 24:
                    child.Text = title
                    break

    class PreferencesPage(_WinUIControl):
        """Preferences page implementation."""
        def __init__(self, title: str = None):
            """Initialize a new preferences page."""
            self._obj = StackPanel()
            self._obj.Orientation = 1  # Vertical
            
            # Add title
            if title:
                title_text = TextBlock()
                title_text.Text = title
                title_text.FontSize = 24
                self._obj.Children.Append(title_text)

        def add(self, group):
            """Add a group to the preferences page."""
            self._obj.Children.Append(group._obj)
            
        def set_title(self, title):
            """Set the title of the preferences page."""
            for i in range(self._obj.Children.Size):
                child = self._obj.Children.GetAt(i)
                if isinstance(child, TextBlock) and child.FontSize == 24:
                    child.Text = title
                    break
            
        def set_icon_name(self, icon_name):
            """Set the icon name of the preferences page."""
            # Would need icon loading logic
            print(f"!!!{self=} set_icon_name, {icon_name=}")

    class SpinRow(_WinUIControl):
        """Spin row implementation."""
        def __init__(self, title=None, adjustment=None):
            """Initialize a new spin row."""
            self._obj = StackPanel()
            self._obj.Orientation = 0  # Horizontal
            
            # Title
            if title:
                title_text = TextBlock()
                title_text.Text = title
                title_text.VerticalAlignment = VerticalAlignment.Center
                title_text.Margin = Thickness(Right=10)
                self._obj.Children.Append(title_text)
                
            # Spinner
            from win32more.Microsoft.UI.Xaml.Controls import NumberBox
            self._spinner = NumberBox()
            if adjustment:
                self._spinner.Minimum = adjustment.minimum if hasattr(adjustment, 'minimum') else 0
                self._spinner.Maximum = adjustment.maximum if hasattr(adjustment, 'maximum') else 100
                self._spinner.SmallChange = adjustment.step_increment if hasattr(adjustment, 'step_increment') else 1
                self._spinner.Value = adjustment.value if hasattr(adjustment, 'value') else 0
            self._obj.Children.Append(self._spinner)
            
        def get_value(self):
            """Get the value of the spin row."""
            return self._spinner.Value
            
        def set_value(self, value):
            """Set the value of the spin row."""
            self._spinner.Value = value

    class StatusPage(_WinUIControl, _Expandable):
        """Status page implementation."""
        def __init__(self, title="", description="", icon_name=None, children=None):
            """Initialize a new status page."""
            self._obj = StackPanel()
            self._obj.Orientation = 1  # Vertical
            self._obj.HorizontalAlignment = HorizontalAlignment.Center
            self._obj.VerticalAlignment = VerticalAlignment.Center

            # Title
            self._title_text = TextBlock()
            self._title_text.Text = title
            self._title_text.FontSize = 24
            self._title_text.Margin = Thickness(Left=10, Top=10, Right=10, Bottom=10)
            self._obj.Children.Append(self._title_text)

            # Description
            self._description_text = TextBlock()
            self._description_text.Text = description
            self._description_text.TextWrapping = 1  # Wrap
            self._description_text.Margin = Thickness(Left=10, Top=10, Right=10, Bottom=10)
            self._obj.Children.Append(self._description_text)

            # Icon (if provided)
            if icon_name:
                # For simplicity, assume icon is a URL or a local file path
                # You might need to handle different types of icons differently
                icon_image = None  # Implement icon loading logic here
                if icon_image:
                    self._obj.Children.Append(icon_image)

            # Children (additional content)
            if children:
                for child in children:
                    self._obj.Children.Append(child.winui_get_obj())

            # Optional progress bar for loading status
            from win32more.Microsoft.UI.Xaml.Controls import ProgressBar
            self._progress_bar = ProgressBar()
            self._progress_bar.IsIndeterminate = True
            self._progress_bar.Visibility = Visibility.Collapsed
            self._obj.Children.Append(self._progress_bar)

        @staticmethod
        def new(title="", description="", icon=None, children=None):
            """Create a new status page."""
            return Adw.StatusPage(title, description, icon, children)

        def set_title(self, title):
            """Set the title of the status page."""
            self._title_text.Text = title

        def set_description(self, description):
            """Set the description of the status page."""
            self._description_text.Text = description

        def set_icon(self, icon):
            """Set the icon of the status page."""
            # Implement icon loading and updating logic here
            pass

        def set_children(self, children):
            """Set the children of the status page."""
            # Remove existing children except title, description, and progress bar
            for i in range(self._obj.Children.Size - 1, 1, -1):
                child = self._obj.Children.GetAt(i)
                if child != self._progress_bar:
                    self._obj.Children.RemoveAt(i)
                    
            # Add new children
            for child in children:
                self._obj.Children.Append(child.winui_get_obj())

        def show_progress(self, show):
            """Show or hide the progress indicator of the status page."""
            self._progress_bar.Visibility = Visibility.Visible if show else Visibility.Collapsed