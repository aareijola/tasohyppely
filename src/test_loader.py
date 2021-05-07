import unittest
from loader import *
from gamelevel import *


class TestLoader(unittest.TestCase):
    """
    This class tests the loader-class of the platformer game. 
    """

    def testListLevels(self):
        """
        Tests if listLevels can list the filenames of files added to the levels/ directory.
        """

        # Create 3 files with names file0, file1, file2
        lvlnamebase = 'file'
        names = []
        for i in range(3):
            name = lvlnamebase + str(i)
            names.append(name)
            # Save files to directory
            f = open('levels/' + name + '.txt', 'w')
            f.close()
        
        levels = listLevels()
        
        for i in range(3):
            self.assertTrue(names[i] in levels, 
                "testListLevels failed, files not found"
            )

    def testSaveLevel(self):
        """
        Test that saving a real level returns True and that the level file exists in the directory.
        """

        testLevel = GameLevel()
        testLevel.setSpawn(QPointF(123, 123))
        testLevel.setFinish(QPointF(5, 5))
        testLevel.setName("TestLevel1")
        ret = saveLevel(testLevel)
        self.assertTrue(ret,
            "Saving TestLevel returned False, expected True"
        )
        self.assertTrue(
            'TestLevel1' in listLevels(),
            "TestLevel didn't save to levels/ correctly."
        )

    def testSaveBrokenLevel(self):
        """
        Test that saving a broken level returns False.
        """
        testLevel = GameLevel()
        ret = saveLevel(testLevel)
        self.assertTrue(ret is False, 
            "Saving broken level returned True, expected False"
        )

    def testSaveLevelWithObjects(self):
        """
        Tests saving a real, more complicated file returns True and that the level file exists in the directory.
        """
        testLevel = GameLevel()
        testLevel.setSpawn(QPointF(123, 123))
        testLevel.setFinish(QPointF(5, 5))
        
        for i in range(10):
            testLevel.objects.append(
                QGraphicsRectItem(100*i, 0, 50, 50)
            )

        for i in range(10):
            testLevel.objects.append(
                Spike(i * -100, 0)
            )
            
        testLevel.setName("TestLevel2")
        ret = saveLevel(testLevel)
        self.assertTrue(ret,
            "Saving TestLevel returned False, expected True"
        )
        self.assertTrue(
            'TestLevel2' in listLevels(),
            "TestLevel didn't save to levels/ correctly."
        )

    def testLoadLevel(self):
        """
        Tests that loading a level from file produces a playable GameLevel.
        """
        testLevel = GameLevel()
        testLevel.setSpawn(QPointF(123, 123))
        testLevel.setFinish(QPointF(5, 5))
        testLevel.setName("TestLevel1")
        saveLevel(testLevel)
        
        
        level = loadLevel('TestLevel1')
        self.assertTrue(level.isPlayable(),
            "Loading a playable level from file didnt produce a playable level."
        )

    def testLoadCorruptedLevel(self):
        """
        Tests that a file with no save data returns None.
        """
        f = open('levels/brokenlevel.txt', 'w')
        f.write("aaaaa")
        f.close()

        self.assertEqual(loadLevel('brokenlevel'), None)

    def testSaveAndLoad(self):
        """
        Tests that saving a complicated playable level to file and loading it returns the same GameLevel.
        """
        
        level = GameLevel()
        level.setName('bigtestlevel')
        level.setFinish(QPointF(100, 100))
        level.setSpawn(QPointF(0,0))

        for i in range(50):
            level.objects.append(QGraphicsRectItem(50*i, 50*i, 25, 25))
            level.objects.append(Spike(-50*i, -50*i))
        ret = saveLevel(level)

        self.assertTrue(ret,
            "Save didnt return True."
        )

        level2 = loadLevel('bigtestlevel')
        self.assertEqual(level.spawn, level2.spawn)
        self.assertEqual(level.objects[15].pos(), level2.objects[15].pos())
        self.assertEqual(level.spawn, level2.spawn)
        
unittest.main()