#!/usr/bin/python3
"""Unit test module for the FileStorage class."""

import unittest
from datetime import datetime
import time
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage
import re
import json
import os


class TestFileStorage(unittest.TestCase):
    """Test Cases for the FileStorage class."""

    def setUp(self):
        """Sets up test methods."""
        pass

    def resetStorage(self):
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def tearDown(self):
        """Tears down test methods."""
        self.resetStorage()
        pass

    def test_instantiation(self):
        """Tests the instantiation of the storage class."""
        self.assertEqual(type(storage).__name__, "FileStorage")

    def test_init_no_args(self):
        """Tests the __init__ method with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as e:
            FileStorage.__init__()
        msg = "descriptor '__init__' of 'object' object needs an argument"
        self.assertEqual(str(e.exception), msg)

    def test_init_many_args(self):
        """Tests the __init__ method with too many arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as e:
            b = FileStorage(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        msg = "object() takes no parameters"
        self.assertEqual(str(e.exception), msg)

    def test_attributes(self):
        """Tests class attributes."""
        self.resetStorage()
        self.assertTrue(hasattr(FileStorage, "_FileStorage__file_path"))
        self.assertTrue(hasattr(FileStorage, "_FileStorage__objects"))
        self.assertEqual(getattr(FileStorage, "_FileStorage__objects"), {})

    def help_test_all(self, classname):
        """Helper method for testing the all() method."""
        self.resetStorage()
        self.assertEqual(storage.all(), {})

        o = storage.classes()[classname]()
        storage.new(o)
        key = "{}.{}".format(type(o).__name__, o.id)
        self.assertTrue(key in storage.all())
        self.assertEqual(storage.all()[key], o)

    def test_all_base_model(self):
        """Tests the all() method for BaseModel."""
        self.help_test_all("BaseModel")

    def test_all_user(self):
        """Tests the all() method for User."""
        self.help_test_all("User")

    def test_all_state(self):
        """Tests the all() method for State."""
        self.help_test_all("State")

    def test_all_city(self):
        """Tests the all() method for City."""
        self.help_test_all("City")

    def test_all_amenity(self):
        """Tests the all() method for Amenity."""
        self.help_test_all("Amenity")

    def test_all_place(self):
        """Tests the all() method for Place."""
        self.help_test_all("Place")

    def test_all_review(self):
        """Tests the all() method for Review."""
        self.help_test_all("Review")

    def help_test_all_multiple(self, classname):
        """Helper method for testing the all() method with many objects."""
        self.resetStorage()
        self.assertEqual(storage.all(), {})

        cls = storage.classes()[classname]
        objs = [cls() for i in range(1000)]
        [storage.new(o) for o in objs]
        self.assertEqual(len(objs), len
