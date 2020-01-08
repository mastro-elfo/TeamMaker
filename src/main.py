#!/usr/bin/env python

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from Handler import Handler

if __name__ == "__main__":
    style_provider = Gtk.CssProvider()
    style_provider.load_from_path("./style.css")
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
    )

    builder = Gtk.Builder()
    builder.add_from_file("TeamMaker.glade")
    builder.connect_signals(Handler(builder))

    window = builder.get_object("MainWindow")
    window.show_all()

    Gtk.main()
