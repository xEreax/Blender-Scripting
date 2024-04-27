bl_info = {
    "name": "Bake all image sequences",
    "author": "EDWINA ASUMANG",
    "version": (3),
    "blender": (4, 0, 0),
    "location": "Properties>Physics",
    "description": "Bakes image sequences for all Dynamic Paint canvas surfaces in object",
    "category": "Physics",
}

import bpy

class BakeImageSequencesPanel(bpy.types.Panel):
    """Creates a Panel in the Physics properties window"""
    bl_label = "Bake Image Sequences Panel"
    bl_idname = "PHYSICS_PT_bake_image_sequences"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "physics"

    def draw(self, context):
        row = self.layout.row()
        row.operator("dpaint.bake_image_sequences")

class BakeImageSequences(bpy.types.Operator):
    """Bakes image sequences for all listed Dynamic Paint surfaces"""
    bl_idname = "dpaint.bake_image_sequences"
    bl_label = "Bake Image Sequences"

    canvas_surfaces: bpy.props.IntProperty()
    index: bpy.props.IntProperty()

    def execute(self, context):
        bpy.ops.dpaint.bake()
        return {'FINISHED'}

    def modal(self, context, event):
        if not bpy.context.window_manager.is_interface_locked:
            self.index -= 1
            if self.index < 0:
                return {'FINISHED'}

            context.object.modifiers["Dynamic Paint"].canvas_settings.canvas_surfaces.active_index = self.index
            self.execute(context)

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.canvas_surfaces = len(context.object.modifiers["Dynamic Paint"].canvas_settings.canvas_surfaces)
        self.index = self.canvas_surfaces

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


def register():
    bpy.utils.register_class(BakeImageSequencesPanel)
    bpy.utils.register_class(BakeImageSequences)


def unregister():
    bpy.utils.unregister_class(BakeImageSequencesPanel)
    bpy.utils.unregister_class(BakeImageSequences)


if __name__ == "__main__":
    register()
