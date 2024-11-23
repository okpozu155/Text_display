Bible Verse Display: ASV

Bible Verse Display: ASV is a lightweight GTK-based application that periodically displays random Bible verses from the American Standard Version (ASV) in a minimalist floating window. 
The program is designed for quick inspiration and unobtrusive operation, making it a perfect tool for personal reflection or casual use.

Features

    Random Bible Verses: Automatically fetches and displays a new verse every 10 seconds.
    Customizable Position: Starts in the upper-right corner of the screen but can be dragged to any location using the mouse.
    Always on Top: The window remains above other applications for easy access.
    Minimalist Design: Decor-free floating window with simple control buttons for minimizing or closing the app.
    Compact Display: Line-wrapped verses with a clean, readable font on a black background.

Details

Built With:

    Python
    GTK+ 3
    pythonbible library for retrieving Bible content

Customization:

    Font size, color, and other styles can be adjusted via the embedded CSS.
    The verse refresh rate can be modified in the code (GLib.timeout_add).

How to Use

This application has been tested and works on Linux-based systems.

    Clone the repository:

    git clone https://github.com/your-username/bible-verse-display.git

    Install dependencies:

    pip install pythonbible

    sudo apt-get install python3-gi gir1.2-gtk-3.0

    Run the application:

    python3 app.py

Future Enhancements

    Add support for different Bible translations.
    Implement user customization for refresh rates and font settings via a settings panel.
    Allow users to select specific books, chapters, or the testament to display.
    Add functionality for saving favorite verses to a file.
    Add 'Next' and 'Previous' verse button.

This project is a simple yet effective way to keep the Word of God accessible throughout your day. Contributions and suggestions are welcome! 😊
