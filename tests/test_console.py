#!/usr/bin/python3
"""Unit test for the file storage class
"""
import unittest
import json
import pep8
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models.engine.file_storage import FileStorage
import os


class TestConsoleClass(unittest.TestCase):
    """TestConsoleClass resume
    Args:
        unittest (): Propertys for unit testing
    """

    maxDiff = None

    def setUp(self):
        """ condition to test file saving """
        with open("test.json", 'w'):
            FileStorage._FileStorage__file_path = "test.json"
            FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """ destroys created file """
        FileStorage._FileStorage__file_path = "file.json"
        try:
            os.remove("test.json")
        except FileNotFoundError:
            pass

    def test_module_doc(self):
        """ check for module documentation """
        self.assertTrue(len(HBNBCommand.__doc__) > 0)

    def test_class_doc(self):
        """ check for documentation """
        self.assertTrue(len(HBNBCommand.__doc__) > 0)

    def test_method_docs(self):
        """ check for method documentation """
        for func in dir(HBNBCommand):
            self.assertTrue(len(func.__doc__) > 0)

    def test_pep8(self):
        """ test base and test_base for pep8 conformance """
        style = pep8.StyleGuide(quiet=True)
        file1 = 'console.py'
        file2 = 'tests/test_console.py'
        result = style.check_files([file1, file2])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warning).")

    def test_executable_file(self):
        """ Check if file have permissions to execute"""
        # Check for read access
        is_read_true = os.access('console.py', os.R_OK)
        self.assertTrue(is_read_true)
        # Check for write access
        is_write_true = os.access('console.py', os.W_OK)
        self.assertTrue(is_write_true)
        # Check for execution access
        is_exec_true = os.access('console.py', os.X_OK)
        self.assertTrue(is_exec_true)

    def test_check_help(self):
        """ Verifies that each command has a help output """
        with patch('sys.stdout', new=StringIO()) as help_val:
            HBNBCommand().onecmd("help create")
            self.assertTrue(len(help_val.getvalue()) > 0)
        with patch('sys.stdout', new=StringIO()) as help_val:
            HBNBCommand().onecmd("help all")
            self.assertTrue(len(help_val.getvalue()) > 0)
        with patch('sys.stdout', new=StringIO()) as help_val:
            HBNBCommand().onecmd("help show")
            self.assertTrue(len(help_val.getvalue()) > 0)
        with patch('sys.stdout', new=StringIO()) as help_val:
            HBNBCommand().onecmd("help destroy")
            self.assertTrue(len(help_val.getvalue()) > 0)
        with patch('sys.stdout', new=StringIO()) as help_val:
            HBNBCommand().onecmd("help update")
            self.assertTrue(len(help_val.getvalue()) > 0)

    def test_create_good(self):
        """ Test the create function """
        with patch('sys.stdout', new=StringIO()) as help_val:
            HBNBCommand().onecmd("create BaseModel")
            self.assertTrue(len(help_val.getvalue()) > 0)

    def test_create_empty(self):
        """ Test the create function """
        with patch('sys.stdout', new=StringIO()) as help_val:
            HBNBCommand().onecmd("create")
            self.assertEqual(help_val.getvalue(), "** class name missing **\n")

    def test_create_unknown(self):
        """ Test the create function """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("create Holberton")
            self.assertEqual(val.getvalue(), "** class doesn't exist **\n")

    def test_show(self):
        """ test show with normal parameters """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('create BaseModel')
            basemodel_id = val.getvalue()
            self.assertTrue(len(basemodel_id) > 0)
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('show BaseModel ' + basemodel_id)
            self.assertTrue(val.getvalue() != "** no instance found **\n")

    def test_show_notfound(self):
        """ Test with class that does not exists """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('show helloo ')
            self.assertTrue(val.getvalue() == "** class doesn't exist **\n")

    def test_show_empty(self):
        """ Test with class missing """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('show')
            self.assertTrue(val.getvalue() == "** class name missing **\n")

    def test_show_id(self):
        """ Test with id missing """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('show BaseModel')
            self.assertTrue(val.getvalue() == "** instance id missing **\n")

    def test_destroy_empty(self):
        """ Checks if class is missing """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('destroy')
            self.assertTrue(val.getvalue() == "** class name missing **\n")

    def test_destroy_wrong(self):
        """ Checks if class name does not exists """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('destroy fakeclass')
            self.assertTrue(val.getvalue() == "** class doesn't exist **\n")

    def test_destroy_id(self):
        """ Check if the id is missing """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('destroy BaseModel')
            self.assertTrue(val.getvalue() == "** instance id missing **\n")

    def test_destroy_notfound(self):
        """ Checks is the id belongs to an instance """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('create BaseModel')
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('destroy BaseModel 121212')
            self.assertTrue(val.getvalue() == "** no instance found **\n")

    def destroy_working(self):
        """ Checks is destroy methods deletes succesfully an instance """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('create BaseModel')
            basemodel_id = val.getvalue()
            self.assertTrue(len(basemodel_id) > 0)
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('destroy BaseModel ' + basemodel_id)
            self.assertTrue(val.getvalue() != "** no instance found **\n")

    def test_all_fakeclass(self):
        """ Checks if class name exists """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('create BaseModel')
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('all FakeClass')
            self.assertTrue(val.getvalue() == "** class doesn't exist **\n")

    def test_all_working(self):
        """ Checks if the method all works correclty """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('create BaseModel')
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('all')
            self.assertTrue(len(val.getvalue()) > 0)

    def test_all_trueclass(self):
        """ Checks that the all method works correctly with a class input """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('create BaseModel')
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('all BaseModel')
            self.assertTrue(len(val.getvalue()) > 0)

    def test_update_missingclass(self):
        """ Checks if the class is missing """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('update')
            self.assertTrue(val.getvalue() == "** class name missing **\n")

    def test_update_wrongclass(self):
        """ Checks if the class exists """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('create BaseModel')
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('update FakeClass')
            self.assertTrue(val.getvalue() == "** class doesn't exist **\n")

    def test_update_noinstance(self):
        """ Checks is the instance id is missing """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('create BaseModel')
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('update BaseModel')
            self.assertTrue(val.getvalue() == "** instance id missing **\n")

    def test_update_notfound(self):
        """ Checks is instance id exists """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('create BaseModel')
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('update BaseModel 121212')
            self.assertTrue(val.getvalue() == "** no instance found **\n")

    def test_update_missing_name(self):
        """ Checks if the attribute name is missing """
        with patch('sys.stdout', new=StringIO()) as my_id:
            HBNBCommand().onecmd('create BaseModel')
            basemodel_id = my_id.getvalue()
            self.assertTrue(len(basemodel_id) > 0)
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('update BaseModel ' + basemodel_id)
            self.assertTrue(val.getvalue() == "** attribute name missing **\n")

    def test_update_missing_value(self):
        """ Checks if the attribute value is missing """
        with patch('sys.stdout', new=StringIO()) as my_id:
            HBNBCommand().onecmd('create BaseModel')
            base_id = my_id.getvalue()
            self.assertTrue(len(base_id) > 0)
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd('update BaseModel ' + base_id + "first_name")
            self.assertTrue(val.getvalue() == "** value missing **\n")

    def test_update_ok(self):
        """ update test working """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("create BaseModel")
            user_id = val.getvalue()
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("update BaseModel " + user_id + " name betty")
            HBNBCommand().onecmd("show BaseModel " + user_id)
            self.assertTrue("betty" in val.getvalue())

    def test_update_okextra(self):
        """ update test working """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("create BaseModel")
            uid = val.getvalue()
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("update BaseModel " + uid + " name betty ho")
            HBNBCommand().onecmd("show BaseModel " + uid)
            self.assertTrue("betty" in val.getvalue())

    def test_user_console(self):
        """ Test the class user with console """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("create User")
            user_id = val.getvalue()
            self.assertTrue(user_id != "** class doesn't exist **\n")
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("show User " + user_id)
            self.assertTrue(val.getvalue() != "** no instance found **\n")
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("all User")
            self.assertTrue(val.getvalue() != "** class doesn't exist **\n")
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("update User " + user_id + " name betty")
            HBNBCommand().onecmd("show User " + user_id)
            self.assertTrue("betty" in val.getvalue())
            HBNBCommand().onecmd("destroy User " + user_id)
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("show User "+user_id)
            self.assertEqual(val.getvalue(), "** no instance found **\n")

    def test_place_console(self):
        """ Test the class user with console """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("create Place")
            user_id = val.getvalue()
            self.assertTrue(user_id != "** class doesn't exist **\n")
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("show Place " + user_id)
            self.assertTrue(val.getvalue() != "** no instance found **\n")
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("all Place")
            self.assertTrue(val.getvalue() != "** class doesn't exist **\n")
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("update Place " + user_id + " name betty")
            HBNBCommand().onecmd("show Place " + user_id)
            self.assertTrue("betty" in val.getvalue())
            HBNBCommand().onecmd("destroy Place " + user_id)
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("show Place "+user_id)
            self.assertEqual(val.getvalue(), "** no instance found **\n")

    def test_state_console(self):
        """ Test the class user with console """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("create State")
            user_id = val.getvalue()
            self.assertTrue(user_id != "** class doesn't exist **\n")
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("show State " + user_id)
            self.assertTrue(val.getvalue() != "** no instance found **\n")
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("all State")
            self.assertTrue(val.getvalue() != "** class doesn't exist **\n")
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("update State " + user_id + " name betty")
            HBNBCommand().onecmd("show State " + user_id)
            self.assertTrue("betty" in val.getvalue())
            HBNBCommand().onecmd("destroy State " + user_id)
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("show State "+user_id)
            self.assertEqual(val.getvalue(), "** no instance found **\n")

    def test_city_console(self):
        """ Test the class user with console """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("create City")
            user_id = val.getvalue()
            self.assertTrue(user_id != "** class doesn't exist **\n")
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("show City " + user_id)
            self.assertTrue(val.getvalue() != "** no instance found **\n")
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("all City")
            self.assertTrue(val.getvalue() != "** class doesn't exist **\n")
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("update City " + user_id + " name betty")
            HBNBCommand().onecmd("show City " + user_id)
            self.assertTrue("betty" in val.getvalue())
            HBNBCommand().onecmd("destroy City " + user_id)
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("show City "+user_id)
            self.assertEqual(val.getvalue(), "** no instance found **\n")

    def test_amenity_console(self):
        """ Test the class user with console """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("create Amenity")
            user_id = val.getvalue()
            self.assertTrue(user_id != "** class doesn't exist **\n")
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("show Amenity " + user_id)
            self.assertTrue(val.getvalue() != "** no instance found **\n")
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("all Amenity")
            self.assertTrue(val.getvalue() != "** class doesn't exist **\n")
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("update Amenity " + user_id + " name betty")
            HBNBCommand().onecmd("show Amenity " + user_id)
            self.assertTrue("betty" in val.getvalue())
            HBNBCommand().onecmd("destroy Amenity " + user_id)
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("show Amenity "+user_id)
            self.assertEqual(val.getvalue(), "** no instance found **\n")

    def test_review_console(self):
        """ Test the class user with console """
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("create Review")
            user_id = val.getvalue()
            self.assertTrue(user_id != "** class doesn't exist **\n")
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("show Review " + user_id)
            self.assertTrue(val.getvalue() != "** no instance found **\n")
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("all Review")
            self.assertTrue(val.getvalue() != "** class doesn't exist **\n")
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("update Review " + user_id + " name betty")
            HBNBCommand().onecmd("show Review " + user_id)
            self.assertTrue("betty" in val.getvalue())
            HBNBCommand().onecmd("destroy Review " + user_id)
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("show Review "+user_id)
            self.assertEqual(val.getvalue(), "** no instance found **\n")

    def test_alternative_all(self):
        """test alternative all with [class].all"""
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("User.all()")
            self.assertTrue(len(val.getvalue()) > 0)

    def test_alternative_show(self):
        """test alternative show with [class].show"""
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("create User")
            user_id = val.getvalue()
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("User.show(\"" + user_id + "\")")
            self.assertTrue(len(val.getvalue()) > 0)

    def test_count(self):
        """test alternative show with [class].show"""
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("User.count()")
            self.assertTrue(int(val.getvalue()) == 0)
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("User.count()")
            self.assertTrue(int(val.getvalue()) == 1)

    def test_alternative_destroy(self):
        """test alternative destroy with [class].destroy(id)"""
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("create User")
            user_id = val.getvalue()
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("User.destroy(\"" + user_id + "\")")
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("User.count()")
            self.assertTrue(int(val.getvalue()) == 0)

    def test_alternative_update1(self):
        """test alternative update with [class].show"""
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("create User")
            user_id = val.getvalue()
        with patch('sys.stdout', new=StringIO()) as val:
            line = "\", \"name\", \"betty\")"
            HBNBCommand().onecmd("User.update(\"" + user_id + line)
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("User.show(\"" + user_id + "\")")
            self.assertTrue("betty" in val.getvalue())

    def test_alternative_update2(self):
        """test alternative update with [class].show"""
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("create User")
            user_id = val.getvalue()
        with patch('sys.stdout', new=StringIO()) as val:
            line = "\", {'first_name': 'John', 'age': 89})"
            HBNBCommand().onecmd("User.update(\"" + user_id + line)
        with patch('sys.stdout', new=StringIO()) as val:
            HBNBCommand().onecmd("User.show(\"" + user_id + "\")")
            self.assertTrue("John" in val.getvalue())

if __name__ == '__main__':
    unittest.main()
