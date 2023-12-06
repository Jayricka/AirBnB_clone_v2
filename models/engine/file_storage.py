#!/usr/bin/python3
"""Module for FileStorage class."""
import json
import os
from models.base_model import BaseModel


class FileStorage:
    """Class to manage serialization and deserialization of instances."""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return a dictionary of objects."""
        if cls is None:
            return FileStorage.__objects

        return {
            k: v
            for k, v in FileStorage.__objects.items()
            if isinstance(v, cls)
        }

    def new(self, obj):
        """Add a new object to the dictionary."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Save the serialized objects to the file."""
        serialized_objects = {
            key: obj.to_dict()
            for key, obj in FileStorage.__objects.items()
        }

        with open(FileStorage.__file_path, 'w', encoding='utf-8') as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """Reload objects from the file."""
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as file:
                objects_dict = json.load(file)
                for key, value in objects_dict.items():
                    class_name, obj_id = key.split('.')
                    obj = eval(class_name)(**value)
                    FileStorage.__objects[key] = obj
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete an object from __objects if it exists."""
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            FileStorage.__objects.pop(key, None)
