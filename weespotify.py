# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Jelle van der Waa <jelle@vdwaa.nl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

SCRIPT_NAME = 'weespotify'
SCRIPT_AUTHOR = 'Jelle van der Waa <jelle@vdwaa.nl>'
SCRIPT_VERSION = '1.0'
SCRIPT_LICENSE = 'GPL3'
SCRIPT_DESC = 'Show now playing information from spotify using dbus'
SCRIPT_COMMAND = 'np'

IMPORT_OK = True
try:
    import weechat
except ImportError:
    print('This script must be run under WeeChat.')
    print('Get WeeChat now at: http://www.weechat.org/')
    IMPORT_OK = False

try:
    import dbus
    from dbus.exceptions import DBusException
except ImportError:
    print('You need to have python-dbus installed')
    IMPORT_OK = False

settings = {
        "np_format": ("/me is listening to: {album} - {track}", "Now playing format string options: {artist}, {title}, {album}, {spotifyurl}")
}


def np_cb(data, buf, args):
    """Command "/np": display spotify artist - track"""
    bus = dbus.SessionBus()
    player = bus.get_object('com.spotify.qt', '/')
    iface = dbus.Interface(player, 'org.freedesktop.MediaPlayer2')
    info = iface.GetMetadata()
    title = info['xesam:title']
    artist = info['xesam:artist'][0]
    album = info['xesam:album']
    url = info['xesam:url']

    np = weechat.config_get_plugin('np_format').format(album=album, title=title, artist=artist, spotifyurl=url).encode('utf-8')
    weechat.command(buf, np)
    return weechat.WEECHAT_RC_OK

def main():
    """Main"""
    if not weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC,'', ''):
        return
    for option, (default_value, description) in settings.items():
        if weechat.config_get_plugin(option) == "":
            weechat.config_set_plugin(option, default_value)
        if description:
            weechat.config_set_desc_plugin(option, description)
    weechat.hook_command(SCRIPT_COMMAND,
            SCRIPT_DESC,
            '',
            '',
            '%(buffers_names)',
            'np_cb', '')

if __name__ == "__main__" and IMPORT_OK:
    main()
