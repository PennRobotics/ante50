ante50
======
> _meson branch_

As an example of how GNOME Builder would do this... We need to prepare GTK+ and gobject-introspection in a Python 3 script, so a **meson.build** file should be made with these as installation requirements.

Then, the goal would be to create and run an independent Python script based on the [Python GTK+ 3 Tutorial](https://python-gtk-3-tutorial.readthedocs.io/en/latest/index.html)

(So far, my impression is that meson is not making any installation steps easier for Python sources.)


## Instructions (TODO)

`python3 -m pip install meson`

`python3 -m pip install ninja`

Install cairo (e.g. libcairo)

`pip install PyGObject`

Install gobject-instrospection (from package manager or source)

Install gtk4 development files

`meson setup build`

`cd build`

`ninja`

## Contributing

Feel free to create Issues or Pull Requests, or to fork this and make it awesome, or to make your own competing software

