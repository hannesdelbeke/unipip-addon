bl_info = {
    "name": "PipQt Python Module Manager (PIP)",
    "author": "Hannes",
    "version": (0, 0, 1),
    "blender": (2, 91, 0),
    "location": "TODO add menu",
    "description": "Manage Python modules inside Blender with PIP",
    "support": "COMMUNITY",
    "category": "Development",
}

__version__ = ".".join(map(str, bl_info["version"]))

import bpy
from pathlib import Path


user_scripts_path = Path(bpy.utils.script_path_user())
pth_path = user_scripts_path / "addons/modules"
startup_path = user_scripts_path / "startup"


def create_pth_startup_file():  # startup_path, pth_path
    """
    Creates a file in Blender's startup scripts folder,
    that adds a path to sitedirs to process .pth files on Blender startup.
    startup_path: the path where to create the startup file
    pth_path: the path to add to site packages on startup
    """
    global startup_path
    global pth_path
    # startup_path = Path(startup_path)
    startup_path.mkdir(parents=True, exist_ok=True)  # startup folder might not exist
    file_path = startup_path / "blender_pth_startup.py"

    # TODO read in a text file of paths, or a .pth file
    # so we can add multiple paths in there.
    if not file_path.exists():
        with open(file_path, "w") as f:
            text = "# this file was generated by the blender_pip addon\n" \
            "# it enables support for editable pip installs to the modules folder\n" \
            f"site.addsitedir(r'{pth_path}')\n" \
            "import site\n"
            f.write(text)

    import site
    site.addsitedir(pth_path)


class PipQtPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout


class PipQtOperator(bpy.types.Operator):
    bl_idname = "wm.pip_qt_operator"
    bl_label = "pip installer"
    # window = None

    def execute(self, context):
        create_pth_startup_file()

        global pth_path
        global window

        import pip_qt
        
        pip_qt.py_pip.default_target_path = pth_path  # todo remove reference of py pip in this module
        window = pip_qt.show()
        
        return {'FINISHED'}


def menu_func(self, context):
    layout = self.layout
    layout.operator("wm.pip_qt_operator")


def register():
    bpy.utils.register_class(PipQtOperator)
    bpy.utils.register_class(PipQtPreferences)
    bpy.types.TOPBAR_MT_window.append(menu_func)


def unregister():
    bpy.utils.unregister_class(PipQtOperator)
    bpy.utils.unregister_class(PipQtPreferences)
    bpy.types.TOPBAR_MT_window.remove(menu_func)


if __name__ == "__main__":
    register()
