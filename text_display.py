import gi
import random
import pythonbible as Bible
from gi.repository import Gtk, Gdk, GLib

gi.require_version('Gtk', '3.0')
gi.require_version('GLib', '2.0')

class TextDisplayApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Bible Verse Display: ASV")
        
        # Set window properties
        self.set_default_size(300, 100)
        self.set_keep_above(True)  # Keep window above others
        self.set_decorated(False)

        # Set the position to the upper-right corner of the screen
        screen = Gdk.Screen.get_default()
        screen_width = screen.get_width()
        self.set_position(Gtk.WindowPosition.NONE)  # Allows precise control with move()
        self.move(screen_width - 320, 10)  # Position with some padding from the edges

        # Enable mouse dragging
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect("button-press-event", self.on_button_press_event)
        self.connect("motion-notify-event", self.on_motion_notify_event)
        self.drag_start_position = None

        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_box)

        # Header box
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        main_box.pack_start(header_box, False, False, 0)

        # Program name label
        title_label = Gtk.Label(label="Bible Verse Display: ASV")
        header_box.pack_start(title_label, True, True, 0)

        # Control buttons
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        header_box.pack_end(button_box, False, False, 0)

        minimize_button = Gtk.Button(label="_", relief=Gtk.ReliefStyle.NONE)
        minimize_button.connect("clicked", self.minimize_window)
        button_box.pack_start(minimize_button, False, False, 0)

        close_button = Gtk.Button(label="X", relief=Gtk.ReliefStyle.NONE)
        close_button.connect("clicked", Gtk.main_quit)
        button_box.pack_start(close_button, False, False, 0)

        # Text display area
        self.label = Gtk.Label()
        self.label.set_line_wrap(True)
        self.label.set_line_wrap_mode(Gtk.WrapMode.WORD)
        self.label.set_justify(Gtk.Justification.LEFT)  # Gtk.Justification.CENTER
        self.label.set_max_width_chars(30)
        main_box.pack_start(self.label, True, True, 10)
        
        # Apply CSS
        css = b"""
        label {
            font-size: 20px;
            color: #FFFFFF;
            background-color: #000000;
        }
        """
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css)

        context = Gtk.StyleContext()
        context.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
        # Update the label with a random text
        self.update_text()
        
        # Refresh the text every 10 seconds
        GLib.timeout_add(10000, self.update_text)

    def update_text(self):
        try:
            reference, verse = self.get_random_verse()
            self.label.set_text(f"{reference}\n{verse}")
        except Bible.errors.VersionMissingVerseError as e:
            print(f"Error: {e}")
            self.label.set_text(f"{Bible.get_verse_text(43003016)}")
        return True  # Continue calling this function

    def get_random_verse(self):
        books = list(Bible.Book)
        random_book = random.choice(books)
        num_chapters = Bible.get_number_of_chapters(random_book)
        random_chapter = random.randint(1, num_chapters)
        num_verses = Bible.get_number_of_verses(random_book, random_chapter)
        random_verse = random.randint(1, num_verses)
        reference = Bible.get_verse_id(random_book, random_chapter, random_verse)
        verse_text = Bible.get_verse_text(reference)
        normalized_reference = Bible.convert_verse_ids_to_references([reference])
        verse = Bible.format_scripture_references(normalized_reference)
        return verse_text, verse

    def minimize_window(self, button):
        self.iconify()

    def on_button_press_event(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:  # Left mouse button
            self.drag_start_position = (event.x_root, event.y_root)

    def on_motion_notify_event(self, widget, event):
        if self.drag_start_position:
            delta_x = event.x_root - self.drag_start_position[0]
            delta_y = event.y_root - self.drag_start_position[1]
            window_x, window_y = self.get_position()
            self.move(window_x + delta_x, window_y + delta_y)
            self.drag_start_position = (event.x_root, event.y_root)

def main():
    app = TextDisplayApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
