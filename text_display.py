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
        self.set_default_size(300, 150)
        self.set_keep_above(True)  # Keep window above others
        self.set_decorated(False)

        # Set the position to the upper-right corner of the screen
        screen = Gdk.Screen.get_default()
        screen_width = screen.get_width()
        self.set_position(Gtk.WindowPosition.NONE)  # Allows precise control with move()
        self.move(screen_width - 320, 10)  # Position with some padding from the edges

        # Initialize variables
        self.verse_history = []  # Stores the verse history
        self.current_index = -1  # Tracks the current verse index

        # Variables for click-and-drag
        self.drag_start_x = 0
        self.drag_start_y = 0

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
        self.label.set_justify(Gtk.Justification.LEFT)
        self.label.set_max_width_chars(30)
        main_box.pack_start(self.label, True, True, 10)

        # Navigation buttons
        nav_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        main_box.pack_start(nav_box, False, False, 0)

        prev_button = Gtk.Button(label="<<")
        prev_button.connect("clicked", self.show_previous_verse)
        nav_box.pack_start(prev_button, True, True, 0)

        next_button = Gtk.Button(label=">>")
        next_button.connect("clicked", self.show_next_verse)
        nav_box.pack_start(next_button, True, True, 0)

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
        
        # Display the first verse
        self.update_text()

        # Start the auto-update timer (20 seconds)
        self.start_auto_update_timer()

        # Enable click-and-drag functionality
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON_MOTION_MASK)
        self.connect("button-press-event", self.on_button_press)
        self.connect("motion-notify-event", self.on_motion_notify)

    def update_text(self, new_verse=True):
        if new_verse:
            try:
                reference, verse = self.get_random_verse()
                self.verse_history.append(f"{reference}\n{verse}")
                self.current_index = len(self.verse_history) - 1
            except Bible.errors.VersionMissingVerseError as e:
                print(f"Error: {e}")
                self.verse_history.append("Error fetching verse.")
                self.current_index = len(self.verse_history) - 1

        self.label.set_text(self.verse_history[self.current_index])

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

    def show_previous_verse(self, button):
        if self.current_index > 0:
            self.current_index -= 1
            self.label.set_text(self.verse_history[self.current_index])

    def show_next_verse(self, button=None):
        if self.current_index < len(self.verse_history) - 1:
            self.current_index += 1
            self.label.set_text(self.verse_history[self.current_index])
        else:
            self.update_text()

    def start_auto_update_timer(self):
        GLib.timeout_add_seconds(20, self.auto_update)

    def auto_update(self):
        self.show_next_verse()
        return True  # Continue the timer

    def on_button_press(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
            self.drag_start_x, self.drag_start_y = event.x_root, event.y_root

    def on_motion_notify(self, widget, event):
        if event.state & Gdk.ModifierType.BUTTON1_MASK:
            delta_x = event.x_root - self.drag_start_x
            delta_y = event.y_root - self.drag_start_y
            self.drag_start_x, self.drag_start_y = event.x_root, event.y_root
            pos_x, pos_y = self.get_position()
            self.move(pos_x + delta_x, pos_y + delta_y)

def main():
    app = TextDisplayApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
