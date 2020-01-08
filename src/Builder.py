class Builder(object):
    def __init__(self, builder, *args, **kwargs):
        super(Builder, self).__init__(*args, **kwargs)
        self.builder = builder

    # Getters
    def get_object(self, id):
        return self.builder.get_object(id)

    def get_text(self, id):
        return self.get_object(id).get_text()

    def get_value(self, id):
        return self.get_object(id).get_value()

    def get_active(self, id):
        return self.get_object(id).get_active()

    def get_selected(self, id):
        return self.get_object(id).get_selected()

    def get_selected_rows(self, id):
        return self.get_object(id).get_selected_rows()

    def count_selected_rows(self, id):
        return self.get_object(id).count_selected_rows()

    # Setters
    def set_sensitive(self, id, sensitive):
        return self.get_object(id).set_sensitive(sensitive)

    def set_text(self, id, value):
        self.get_object(id).set_text(value)

    def set_value(self, id, value):
        self.get_object(id).set_value(value)

    def set_active(self, id, active):
        self.get_object(id).set_active(active)

    def set_visible(self, id, visible):
        self.get_object(id).set_visible(visible)

    # is-ers
    def is_visible(self, id):
        """https://lazka.github.io/pgi-docs/Gtk-3.0/classes/Widget.html#Gtk.Widget.get_visible"""
        return self.get_object(id).is_visible()
