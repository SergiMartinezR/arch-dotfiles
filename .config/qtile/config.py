# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile import hook

from os import path
import subprocess


@hook.subscribe.startup_once
def autostart():
    qtile_path = path.join(path.expanduser('~'), ".config", "qtile")
    subprocess.call([path.join(qtile_path, 'autostart.sh')])

colors = []
cache='/home/sergi/.cache/wal/colors'
def load_colors(cache):
    with open(cache, 'r') as file:
        for i in range(8):
            colors.append(file.readline().strip())
    colors.append('#ffffff')
    lazy.reload()
load_colors(cache)

mod = "mod4"
terminal = "kitty"

keys = [
    # Switch between windows
    Key([mod], "a", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "d", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "s", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "w", lazy.layout.up(), desc="Move focus up"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "a", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "d", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "s", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "w", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "a", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "d", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "s", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "w", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),

    ##SPAWN APPS
    #Spawns a terminal
    Key([mod], "space", lazy.spawn(terminal), desc="Launch terminal"),
    #Spawns a browser
    Key([mod], "b", lazy.spawn('firefox'), desc="Launch a browser"),
    #Spawns spotify
    Key([mod], "XF86Tools", lazy.spawn('spotify'), desc="Launch spotify"),
    #Spawns Visual Studio Code
    Key([mod], "q", lazy.spawn('rofi -show run'), desc="Launch VSCode"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([mod], "e", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
]

groups = [Group(i) for i in [
    "  ", "  ", "  ", "  ", "  ", " ﭮ ", " 調 ", "  ", " 拾 ",
]]

for i, group in enumerate(groups):
    actual_key = str(i + 1)
    keys.extend([
        # Switch to workspace N
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        # Send window to workspace N and switch to that group
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name, switch_group=True)),
        # Just send window to workspace N
        Key([mod, "control"], actual_key, lazy.window.togroup(group.name))
    ])

layouts = [
    layout.Columns(border_focus='#bb69fb', border_width=0, margin=4, fair=True),
    layout.Max()
]

def base(fg=colors[0], bg=colors[0]): 
    return {
        'foreground': fg,
        'background': bg
    }


def separator():
    return widget.Sep(**base(), linewidth=0, padding=190)


def icon(fg=colors[0], bg=colors[0], fontsize=16, text="?"):
    return widget.TextBox(
        **base(fg, bg),
        fontsize=fontsize,
        text=text,
        padding=3
    )


def powerline(fg=colors[0], bg=colors[0]):
    return widget.TextBox(
        **base(fg, bg),
        text="", # Icon: nf-oct-triangle_left
        fontsize=37,
        padding=8.2  #Modify this value till the triangle is fully connected to the box
    )

def workspaces(): 
    return [
        widget.Sep(**base(), linewidth=0, padding=5),
        widget.GroupBox(
            **base(),
            font='Hurmit Nerd Font',
            fontsize=19,
            margin_y=3,
            margin_x=0,
            padding_y=8,
            padding_x=5,
            borderwidth=1,
            active=colors[7],
            inactive=colors[3],
            rounded=True,
            highlight_method='block',
            urgent_alert_method='block',
            urgent_border=colors[2],
            this_current_screen_border=colors[5],
            this_screen_border=colors[5],
            other_current_screen_border=colors[6],
            other_screen_border=colors[6],
            use_mouse_wheel = False,
            disable_drag=True
        ),
        separator(),
    ]

def parse_text_func(wname: str):
    wname = wname[::-1]
    index = wname.find(" ")
    if index != -1:
        wname = wname[0:index]
        wname = wname[::-1]
        return " " + wname
    else:
        wname = wname[::-1]
        return " " + wname

primary_widgets = [

    *workspaces(),

    separator(),

    powerline(colors[3], colors[0]),

    widget.WindowName(**base(fg=colors[0], bg=colors[3]), fontsize=14, empty_group_string='', parse_text=parse_text_func),

    powerline(colors[2], colors[3]),

    icon(fg=colors[0], bg=colors[2], text=' '), # Icon: nf-fa-download
    
    widget.GenPollText(
        **base(colors[0], colors[2]),
        fontsize=14,
        func=lambda: (subprocess.check_output("/home/sergi/.config/qtile/Scripts/iphtb.sh").decode("utf-8")),
        padding=3,
        update_interval=2
    ),
    
    powerline(colors[4], colors[2]),

    icon(fg=colors[0],bg=colors[4],text=' '),  # Icon: nf-fa-feed

    widget.GenPollText(
        **base(colors[0], colors[4]),
        fontsize=14,
        func=lambda: (subprocess.check_output("/home/sergi/.config/qtile/Scripts/ip.sh").decode("utf-8")),
        padding=3,
        update_interval=2
    ),

    powerline(colors[5], colors[4]),

    icon(fg=colors[0],bg=colors[5],text='墳 '),

    widget.PulseVolume(**base(bg=colors[5]), volume_app="pactl", padding=5),

    powerline(colors[6], colors[5]),

    icon(fg=colors[0],bg=colors[6], fontsize=17, text=' '), # Icon: nf-mdi-calendar_clock

    widget.Clock(**base(fg=colors[0],bg=colors[6]), format='%d/%m/%Y - %H:%M'),

    powerline(colors[7], colors[6]),

    icon(fg=colors[0],bg=colors[7], fontsize=17, text=' '), # Icon: nf-mdi-calendar_clock
    
    widget.CPU(foreground=colors[0], background=colors[7], padding=5, format='{load_percent}%'),
]

secondary_widgets = [
        widget.GroupBox(
            **base(),
            font='Hurmit Nerd Font',
            fontsize=17,
            margin_y=3,
            margin_x=0,
            padding_y=8,
            padding_x=5,
            borderwidth=1,
            active=colors[7],
            inactive=colors[3],
            rounded=True,
            highlight_method='block',
            urgent_alert_method='block',
            urgent_border=colors[2],
            this_current_screen_border=colors[5],
            this_screen_border=colors[5],
            other_current_screen_border=colors[6],
            other_screen_border=colors[6],
            use_mouse_wheel = False,
            disable_drag=True
        ),

    widget.Sep(**base(), linewidth=0, padding=160),

    powerline(colors[3], colors[0]),

    widget.WindowName(**base(fg=colors[0], bg=colors[3]), fontsize=14, empty_group_string='', parse_text=parse_text_func),

    powerline(colors[2], colors[3]),

    icon(fg=colors[0], bg=colors[2], text='? '),

    powerline(colors[4], colors[2]),

    icon(fg=colors[0],bg=colors[4],text='? '),  # Icon: nf-fa-feed

    widget.Net(**base(bg=colors[4])),
    
    powerline(colors[5], colors[4]),

    icon(fg=colors[0],bg=colors[5],text='? '),

    powerline(colors[6], colors[5]),

    icon(fg=colors[0],bg=colors[6], fontsize=17, text=' '), # Icon: nf-mdi-calendar_clock

    widget.Clock(**base(fg=colors[0],bg=colors[6]), format='%d/%m/%Y - %H:%M '),

    powerline(colors[7], colors[6]),

    icon(fg=colors[0],bg=colors[7], fontsize=17, text='? '), # Icon: nf-mdi-calendar_clock
    
    #widget.CPU(foreground=colors[0], background=colors[6], padding=5, format='{load_percent}%'),
]

widget_defaults = dict(
    font='Hurmit Nerd Font Bold',
    fontsize=14,
    padding=1,
)
extension_defaults = widget_defaults.copy()

screens = [Screen(top=bar.Bar(primary_widgets,24,opacity = 1.0))]

screens.append(Screen(top=bar.Bar(secondary_widgets,24,opacity = 1.0)))

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(border_width=0, float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
