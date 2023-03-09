#!/usr/bin/python3
"""This module contains the Filetorage class"""
import json
from models.base_model import BaseModel
from models.user import User
"""The json module for serializaion and deserialization"""


class FileStorage:
    """The FileStorage class that serializes instances to
        a JSON file and deserializes JSON file to instances
        Args:
            __file_path: Private class attribute
             string - path to the JSON file
             __objects: private class attribute
             dictionary - empty but will store all objects
        """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ returns the dictionary __objects """

        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""

        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """ serializes __objects to the JSON file """
        path = FileStorage.__file_path

        new_obj = {k: FileStorage.__objects[k].to_dict(
        ) for k in FileStorage.__objects.keys()}

        with open(path, "w") as file:
            json.dump(new_obj, file)

    def reload(self):
        path = FileStorage.__file_path

        try:
            with open(path) as file:
                object_json = json.load(file)
                for obj in object_json.values():
                    class_name = obj['__class__']
                    del obj['__class__']
                    self.new(eval(class_name)(**obj))

        except FileNotFoundError:
            return
