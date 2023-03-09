#!/usr/bin/python3
"""This module contains the class BaseModel"""

import uuid
from datetime import datetime
import models


class BaseModel:
    """The BaseModel class that defines all common attributes
            and methods of other classes
    """

    def __init__(self, *args, **kwargs):
        """The initialization function
            Args:
                    created_at: datetime - assign with the current
                    datetime when an instance is created
                    updated_at: datetime - assign with the current datetime
                    when an instance is created and it will be updated
                    every time you change your object
                    id: string - assign with an uuid when an instance
                    is created
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key == "updated_at" or key == "created_at":
                    self.__dict__[key] = datetime.fromisoformat(value)
                else:
                    self.__dict__[key] = value
        else:
            models.storage.new(self)

    def __str__(self):
        """Return the print/str representation of the BaseModel instance."""
        clname = self.__class__.__name__
        return "[{}] ({}) {}".format(clname, self.id, self.__dict__)

    def save(self):
        """updates the public instance attribute updated_at with
            the current datetime"""

        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values
        of __dict__ of the instance"""

        dict_copied = self.__dict__.copy()
        dict_copied["__class__"] = self.__class__.__name__
        dict_copied["created_at"] = self.created_at.isoformat()
        dict_copied["updated_at"] = self.updated_at.isoformat()
        return dict_copied
