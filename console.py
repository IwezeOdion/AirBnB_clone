#!/usr/bin/python3
"""This module contains the console.py module"""

from models.base_model import BaseModel
from models.user import User
from models import storage
import cmd
import os


def tokenize(arg: str) -> list:
    """ Splits a string into tokens delimited by space

    Args:
        arg (string): strings to be splitted

    Returns:
        list: list of strings
    """
    token = arg.split(" ")
    return token


class HBNBCommand(cmd.Cmd):
    """The class HBNB that builds a console"""

    prompt = "(hbnb) "
    CLASSNAMES = ["BaseModel"]

    def do_quit(self, arg: str) -> bool:
        """Quit command to exit the program"""

        return True

    def do_create(self, arg: str) -> None:
        """Creates a new instance of BaseModel, saves it
        (to the JSON file) and prints the id
        """

        tokens = tokenize(arg)
        if arg == "":
            print("** class name missing **")
        elif tokens[0] not in HBNBCommand.CLASSNAMES:
            print("** class doesn't exit **")
        else:
            print(eval(tokens[0])().id)
            storage.save()

    def do_clear(self, args: str) -> None:
        """Clear the screen"""
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def do_show(self, arg: str) -> None:
        """ Prints the string representation of an instance
        based on the class name and id
        """

        tokens = tokenize(arg)
        if arg == "":
            print("** class name missing **")
        elif tokens[0] not in HBNBCommand.CLASSNAMES:
            print("** class doesn't exist **")
        elif len(tokens) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(tokens[0], tokens[1])
            if key not in storage.all():
                print("** no instance found **")
            else:
                print(storage.all()[key])

    def do_destroy(self, arg: str) -> None:
        """: Deletes an instance based on the class name and id
        (save the change into the JSON file)
        """

        tokens = tokenize(arg)
        if arg == "":
            print("** class name missing **")
        elif tokens[0] not in HBNBCommand.CLASSNAMES:
            print("* class doesn't exist **")
        elif len(tokens) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(tokens[0], tokens[1])
            if key not in storage.all():
                print("** no instance found **")
            else:
                del storage.all()[key]
                storage.save()

    def do_all(self, arg: str) -> None:
        """ Prints all string representation of all instances based or
        not on the class name. Ex: $ all BaseModel or $ all.
        The printed result must be a list of strings (like the example below)
        If the class name doesn’t exist, print ** class doesn't exist **
        (ex: $ all MyModel)
        """

        tokens = tokenize(arg)
        if len(tokens) == 0:
            print([str(value) for value in storage.all().values()])
        elif tokens[0] not in HBNBCommand.CLASSNAMES:
            print("** class doesn't exist **")
        else:
            temp = [str(v) for k, v in storage.all().items()
                    if k.startswith(tokens[0])]
            print(temp)

    def do_update(self, arg: str) -> None:
        """ Updates the class object

        Args:
            arg (object): class object
        """
        tokens = tokenize(arg)
        object_json = storage.all()
        if arg == "":
            print("** class name missing **")
        elif tokens[0] not in HBNBCommand.CLASSNAMES:
            print("* class doesn't exist **")
        elif len(tokens) < 2:
            print("** instance id missing **")
        elif f"{tokens[0]}.{tokens[1]}" not in object_json.keys():
            print("** no instance found **")
        elif len(tokens) < 3:
            print("** attribute name missing **")

        else:
            print("** value missing **")
            print(type(tokens[1]))

        if len(tokens) == 4:
            obj = object_json[f"{tokens[0]}.{tokens[1]}"]
            if tokens[2] in obj.__class__.__dict__.keys():
                # get the attribute value type for typecast
                val_type = type(obj.__class__.__dict__[tokens[2]])
                obj.__dict__[tokens[2]] = val_type(tokens[3])
            else:
                obj.__dict__[str(tokens[2])] = tokens[3]

        elif type(eval(tokens[2])) == dict:
            obj = objdict[f"{tokens[0]}.{tokens[1]}"]
            for k, v in eval(tokens[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in [str, int, float]):
                    val_type = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = val_type(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

    def do_EOF(self, arg):
        """Handles EOF"""

        raise systemExit

    def emptyline(self):
        """This doesnt do anything when the no command is passed"""

        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
