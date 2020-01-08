import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

from Builder import Builder
from Players import Players
from Player import Player
from TeamMaker import make_best, make_pairs, make_abba
from Pickable.Pickable import dump, load
from update import check_update, download_update, extract_update, install_contents

from os.path import expanduser, join, isfile
from os import makedirs, remove
from time import time

# Some global init
CONFIG_DIR = expanduser(join('~', '.config', 'TeamMaker'))
PLAYERS_PICKLE = join(CONFIG_DIR, 'Players.pickle')
MAKETEAMS_PICKLE = join(CONFIG_DIR, 'MakeTeams.pickle')
makedirs(CONFIG_DIR, exist_ok = True)

class Handler(Builder):
    def __init__(self, *args, **kwargs):
        super(Handler, self).__init__(*args, **kwargs)
        # Load
        self.players = self.load()
        # Update
        self.update_store('PlayersStore', map(lambda x: (
            x.id,
            x.nickname,
            x.number,
            x.rating,
            x.name,
            x.surname,
            x.rating_change
            ), self.players))
        # Status
        self.status('Loaded %d players' %len(self.players))
        # Latest release
        self.__latest = None
        GLib.timeout_add(1000, self.check_update)

    def status(self, message):
        self.get_object('StatusBar').push(0, message)

    def quit(self, *args):
        Gtk.main_quit()

    def popup(self, popover, *args):
        popover.popup()

    def popdown(self, popover, *args):
        popover.popdown()

    def hide(self, window, *args):
        window.hide()
        return True

    def load(self):
        try:
            ps = Players.load(PLAYERS_PICKLE)
            # Add rating_change, new from 1.4
            for p in ps:
                if not hasattr(p, 'rating_change'):
                    p.rating_change = "media-playback-pause"
            return ps
        except:
            return Players()

    def update_store(self, id, list_):
        store = self.get_object(id)
        store.clear()
        for x in list_:
            store.append(x)

    def check_update(self):
        to_update, json = check_update(self.get_object('AboutWindow').get_version())
        if to_update:
            self.set_visible('UpdatesButton', True)
            self.__latest = json
        return False

    # Events
    def on_PlayersSelection_changed(self, selection, *args):
        count = selection.count_selected_rows()
        if count > 0:
            self.set_sensitive('EditButton', True)
            self.set_sensitive('DeleteButton', True)
        else:
            self.set_sensitive('EditButton', False)
            self.set_sensitive('DeleteButton', False)

        if count > 1:
            self.set_sensitive('MakeButton', True)
        else:
            self.set_sensitive('MakeButton', False)

        self.status('Selected %d player(s)' %count)

    def on_ConfirmNewPlayer_clicked(self, *args):
        # Collect data
        data = (
            self.get_text('NewNickname'),
            self.get_text('NewNumber'),
            int(self.get_text('NewRating')),
            self.get_text('NewName'),
            self.get_text('NewSurname')
        )
        player = Player(*data)
        self.players.append(player)
        self.players.dump(PLAYERS_PICKLE)
        self.get_object('PlayersStore').append((player.id, player.nickname, player.number, player.rating, player.name, player.surname))
        self.popdown(self.get_object('NewPopover'))
        self.status('New player: %s, %s' %(data[0], data[1]))

    def on_ConfirmEditPlayer_clicked(self, *args):
        # Collect data
        data = (
            self.get_text('EditNickname'),
            self.get_text('EditNumber'),
            int(self.get_text('EditRating')),
            self.get_text('EditName'),
            self.get_text('EditSurname')
        )
        model, path = self.get_selected_rows('PlayersSelection')
        store = self.get_object('PlayersStore')
        if path is not None:
            selected = model[path]
            player = self.players.find_id(selected[0])
            if player is not None:
                player.update(**dict(zip(('nickname', 'number', 'rating', 'name', 'surname'), data)))
                self.players.dump(PLAYERS_PICKLE)
                store.set(model.get_iter(path), [1, 2, 3, 4, 5], tuple(player)[1:6])
                self.status('Edit player: %s, %s' %(data[0], data[1]))
            else:
                self.status('Error: player not found in list')
        else:
            self.status('Error: no selected player')
        self.popdown(self.get_object('EditPopover'))

    def on_ConfirmDeletePlayer_clicked(self, *args):
        model, path = self.get_selected_rows('PlayersSelection')
        store = self.get_object('PlayersStore')
        count = self.count_selected_rows('PlayersSelection')
        to_remove = [model.get_iter(p) for p in path]
        for selected in path:
            self.players.remove(self.players.find_id(model[selected][0]))
        for rem in to_remove:
            store.remove(rem)
        self.players.dump(PLAYERS_PICKLE)
        self.status('Deleted %d players' %count)
        self.popdown(self.get_object('DeletePopover'))

    def on_MakeLeftSelection_changed(self, selection, *args):
        if selection.count_selected_rows() > 0:
            self.set_sensitive('MakeToRight', True)
        else:
            self.set_sensitive('MakeToRight', False)

    def on_MakeRightSelection_changed(self, selection, *args):
        if selection.count_selected_rows() > 0:
            self.set_sensitive('MakeToLeft', True)
        else:
            self.set_sensitive('MakeToLeft', False)

    def on_UpdateLeftSelection_changed(self, selection, *args):
        if selection.count_selected_rows() > 0:
            self.set_sensitive('UpdateToRight', True)
        else:
            self.set_sensitive('UpdateToRight', False)

    def on_UpdateRightSelection_changed(self, selection, *args):
        if selection.count_selected_rows() > 0:
            self.set_sensitive('UpdateToLeft', True)
        else:
            self.set_sensitive('UpdateToLeft', False)

    def on_NewPopover_show(self, *args):
        self.set_text('NewNickname', '')
        self.set_text('NewNumber', '')
        self.set_text('NewRating', '1000')
        self.set_text('NewName', '')
        self.set_text('NewSurname', '')

    def on_EditPopover_show(self, *args):
        model, path = self.get_selected_rows('PlayersSelection')
        if path is not None:
            selected = model[path]
            player = self.players.find_id(selected[0])
            if player is not None:
                self.set_text('EditNickname', player.nickname)
                self.set_text('EditNumber', player.number)
                self.set_text('EditRating', str(player.rating))
                self.set_text('EditName', player.name)
                self.set_text('EditSurname', player.surname)

    def on_MakePopover_show(self, *args):
        model, path = self.get_selected_rows('PlayersSelection')
        players = list(filter(lambda x: x.id in [model[p][0] for p in path], self.players))
        left_team, right_team = make_best(players)
        self.update_store('MakeLeftStore', map(lambda x: (x.id, x.nickname, x.number, x.rating, x.name, x.surname), left_team))
        self.update_store('MakeRightStore', map(lambda x: (x.id, x.nickname, x.number, x.rating, x.name, x.surname), right_team))

    def on_MakeLeftRightStore_row_changed(self, *args):
        left_team = Players(*[self.players.find_id(p[0]) for p in self.get_object('MakeLeftStore')])
        right_team = Players(*[self.players.find_id(p[0]) for p in self.get_object('MakeRightStore')])
        self.set_text('LeftTeamStrength', str(left_team.strength()))
        self.set_text('LeftTeamChance', str(int(left_team.chance(right_team) *100)) + '%')
        self.set_text('RightTeamStrength', str(right_team.strength()))
        self.set_text('RightTeamChance', str(int(right_team.chance(left_team) *100)) + '%')

    def on_MakeToRight_clicked(self, *args):
        model, path = self.get_selected_rows('MakeLeftSelection')
        left_store = self.get_object('MakeLeftStore')
        right_store = self.get_object('MakeRightStore')
        to_remove = [model.get_iter(p) for p in path]
        for selected in path:
            right_store.append(tuple(model[selected]))
        for rem in to_remove:
            left_store.remove(rem)

    def on_MakeToLeft_clicked(self, *args):
        model, path = self.get_selected_rows('MakeRightSelection')
        left_store = self.get_object('MakeLeftStore')
        right_store = self.get_object('MakeRightStore')
        to_remove = [model.get_iter(p) for p in path]
        for selected in path:
            left_store.append(tuple(model[selected]))
        for rem in to_remove:
            right_store.remove(rem)

    def on_UnselectButton_clicked(self, *args):
        self.get_object('PlayersSelection').unselect_all()
        self.status('Unselected')

    def on_ApplyMakeTeams_clicked(self, *args):
        left_team = Players(*[self.players.find_id(p[0]) for p in self.get_object('MakeLeftStore')])
        right_team = Players(*[self.players.find_id(p[0]) for p in self.get_object('MakeRightStore')])
        dump((left_team, right_team), MAKETEAMS_PICKLE)
        self.status('Saved teams')
        self.popdown(self.get_object('MakePopover'))

    def on_UpdatePopover_show(self, *args):
        if self.count_selected_rows('PlayersSelection') > 1:
            model, path = self.get_selected_rows('PlayersSelection')
            players = [self.players.find_id(model[p][0]) for p in path]
            left_team = Players(*players[:len(players)//2])
            right_team = Players(*players[len(players)//2:])
        else:
            try:
                left_team, right_team = load(MAKETEAMS_PICKLE)
            except:
                self.popdown(self.get_object('UpdatePopover'))
                self.status("Can't load teams")
        self.update_store('UpdateLeftStore', map(lambda x: (x.id, x.nickname, x.number, x.rating, x.name, x.surname, 0, 0), left_team))
        self.update_store('UpdateRightStore', map(lambda x: (x.id, x.nickname, x.number, x.rating, x.name, x.surname, 0, 0), right_team))

    def on_UpdateToRight_clicked(self, *args):
        model, path = self.get_selected_rows('UpdateLeftSelection')
        left_store = self.get_object('UpdateLeftStore')
        right_store = self.get_object('UpdateRightStore')
        to_remove = [model.get_iter(p) for p in path]
        for selected in path:
            right_store.append(tuple(model[selected]))
        for rem in to_remove:
            left_store.remove(rem)

    def on_UpdateToLeft_clicked(self, *args):
        model, path = self.get_selected_rows('UpdateRightSelection')
        left_store = self.get_object('UpdateLeftStore')
        right_store = self.get_object('UpdateRightStore')
        to_remove = [model.get_iter(p) for p in path]
        for selected in path:
            left_store.append(tuple(model[selected]))
        for rem in to_remove:
            right_store.remove(rem)

    def on_UpdateSave_clicked(self, *args):
        left_store = self.get_object('UpdateLeftStore')
        right_store = self.get_object('UpdateRightStore')
        left_team = Players(*[self.players.find_id(p[0]) for p in left_store])
        right_team = Players(*[self.players.find_id(p[0]) for p in right_store])
        left_delta = int(left_team.delta(True, right_team))
        right_delta = int(right_team.delta(False, left_team))
        left_team.update_rating(left_delta, True)
        right_team.update_rating(right_delta, False)
        self.players.dump(PLAYERS_PICKLE)
        if(isfile(MAKETEAMS_PICKLE)):
            remove(MAKETEAMS_PICKLE)
        store = self.get_object('PlayersStore')
        for p in left_team:
            for r in store:
                if r[0] == p.id:
                    r[3] = p.rating
                    r[6] = p.rating_change
        for p in right_team:
            for r in store:
                if r[0] == p.id:
                    r[3] = p.rating
                    r[6] = p.rating_change
        self.popdown(self.get_object('UpdatePopover'))
        self.status("Ratings updated")

    def on_UpdateLeftRightStore_row_changed(self, *args):
        left_store = self.get_object('UpdateLeftStore')
        right_store = self.get_object('UpdateRightStore')
        left_team = Players(*[self.players.find_id(p[0]) for p in left_store])
        right_team = Players(*[self.players.find_id(p[0]) for p in right_store])
        left_delta = int(left_team.delta(True, right_team))
        right_delta = int(right_team.delta(False, left_team))
        for p in left_store:
            p[6] = left_delta
            p[7] = p[3] +left_delta
        for p in right_store:
            p[6] = right_delta
            p[7] = p[3] +right_delta

    def on_AboutButton_clicked(self, *args):
        self.get_object('AboutWindow').present()

    def on_ConfirmDoUpdates_clicked(self, button, *args):
        self.set_text('UpdatesStatus', '')

        if self.__latest is None:
            self.set_text('UpdatesStatus', 'Unexpected error while updating, nothing changed')
            return

        ret, e = download_update(self.__latest['tarball_url'])
        if not ret:
            self.set_text('UpdatesStatus', 'Error while downloading: ' +e)
            return

        ret, e = extract_update()
        if not ret:
            self.set_text('UpdatesStatus', 'Error while extracting archive: ' +e)
            return

        ret, e = install_contents()
        if not ret:
            self.set_text('UpdatesStatus', 'Error while installing contents: ' +e)
            return

        button.set_sensitive(False)
        self.set_text('UpdatesStatus', 'Install complete, restart required')
        self.status('Install complete, restart required')
        # self.popdown(self.get_object('UpdatesPopover'))
