import unittest
import os
from my_storage_engine import FileStorage


class TestFileStorage(unittest.TestCase):

    def setUp(self):
        # Set up a temporary file for testing
        self.temp_file = 'test_file.json'
        with open(self.temp_file, 'w') as f:
            f.write('{}')
        self.storage_engine = FileStorage(self.temp_file)

    def tearDown(self):
        # Remove the temporary file after testing
        os.remove(self.temp_file)

    def test_create_new_object(self):
        # Test creating a new object and storing it in the FileStorage
        class TestClass:
            def __init__(self, id):
                self.id = id

            def to_dict(self):
                return {'id': self.id}

        test_obj = TestClass('test_id')
        self.storage_engine.new(test_obj)
        self.assertEqual(self.storage_engine.all(), {'TestClass.test_id': test_obj})

    def test_save_and_reload(self):
        # Test saving and reloading objects from the FileStorage
        class TestClass:
            def __init__(self, id):
                self.id = id

            def to_dict(self):
                return {'id': self.id}

        test_obj1 = TestClass('test_id1')
        test_obj2 = TestClass('test_id2')
        self.storage_engine.new(test_obj1)
        self.storage_engine.new(test_obj2)
        self.storage_engine.save()

        # Reload the storage engine from the saved file
        new_storage_engine = FileStorage(self.temp_file)
        new_storage_engine.reload()
        self.assertEqual(new_storage_engine.all(), {'TestClass.test_id1': test_obj1, 'TestClass.test_id2': test_obj2})
