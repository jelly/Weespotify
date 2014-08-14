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

def np_cb(data, buf, args):
    """Command "/np": display spotify artist - track"""
    # TODO: fix unicode problems with Motörhead
    # TODO: add Dbus exception
    # TODO: add formatting options in settings :)
    bus = dbus.SessionBus()
    player = bus.get_object('com.spotify.qt', '/')
    iface = dbus.Interface(player, 'org.freedesktop.MediaPlayer2')
    info = iface.GetMetadata()
    title = str(info['xesam:title'])
    artist = str(info['xesam:artist'][0])
    weechat.command(buf,"/me is listening to: %s - %s" % (artist, title))
    return weechat.WEECHAT_RC_OK

def main():
    """Main"""
    if not weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC,'', ''):
        return
    weechat.hook_command(SCRIPT_COMMAND,
            SCRIPT_DESC,
            '',
            '',
            '%(buffers_names)',
            'np_cb', '')

if __name__ == "__main__" and IMPORT_OK:
    main()
