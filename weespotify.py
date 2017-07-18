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

try:
    import weechat
except ImportError:
    print('This script must be run under WeeChat.')
    print('Get WeeChat now at: http://www.weechat.org/')

try:
    import dbus
except ImportError:
    print('You need to have python-dbus installed')

settings = {
        "np_format": ("/me is listening to: {album} - {track}", "Now playing format string options: {artist}, {title}, {album}, {spotifyurl}")
}


def np_cb(data, buf, args):
    """Command "/np": display spotify artist - track"""

    session_bus = dbus.SessionBus()
    spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")
    spotify_properties = dbus.Interface(spotify_bus, "org.freedesktop.DBus.Properties")
    metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")
    title = metadata['xesam:title']
    artist = metadata['xesam:artist'][0]
    album = metadata['xesam:album']
    url = metadata['xesam:url']

    np = weechat.config_get_plugin('np_format').format(album=album.encode('utf-8'), title=title.encode('utf-8'), artist=artist.encode('utf-8'), spotifyurl=url.encode('utf-8'))
    weechat.command(buf, np)
    return weechat.WEECHAT_RC_OK

weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, '', '')

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
