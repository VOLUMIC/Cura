# Copyright (c) 2018 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.

from UM.Logger import Logger
from cura.Machines.Models.BaseMaterialsModel import BaseMaterialsModel

class GenericMaterialsModel(BaseMaterialsModel):

    def __init__(self, parent = None):
        super().__init__(parent)
        self._update()

    def _update(self):

        # Perform standard check and reset if the check fails
        if not self._canUpdate():
            self.setItems([])
            return

        # Get updated list of favorites
        self._favorite_ids = self._material_manager.getFavorites()

        item_list = []

        for root_material_id, container_node in self._available_materials.items():
            metadata = container_node.metadata

            # Only add results for generic materials
            if metadata["brand"].lower() != "generic":
                continue

            # Do not include the materials from a to-be-removed package
            if bool(metadata.get("removed", False)):
                continue

            item = {
                "root_material_id": root_material_id,
                "id":               metadata["id"],
                "GUID":             metadata["GUID"],
                "name":             metadata["name"],
                "brand":            metadata["brand"],
                "material":         metadata["material"],
                "color_name":       metadata["color_name"],
                "color_code":       metadata["color_code"],
                "container_node":   container_node,
                "is_favorite":      root_material_id in self._favorite_ids
            }
            item_list.append(item)

        # Sort the item list alphabetically by name
        item_list = sorted(item_list, key = lambda d: d["name"].upper())

        self.setItems(item_list)
