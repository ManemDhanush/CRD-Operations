import os
import time
import json
import threading

class CRD:
    '''
        Class for performing the given assignment
    '''

    def __init__(self, location = ""):
        '''
            Constructor for initialization of json object (here we use dictionaries)
            Also we give a desired location to check the json file
        '''

        self.myDict = {}
        self.loc = "M:\\Study Material\\CRD\\MyJSON.json"
        self.lock = threading.Lock()

        if location is not "":
            self.loc = location

        if not os.path.exists(self.loc):
            with open(self.loc, 'w') as file:
                file.write('{}')

        jsonString = ""
        with open(self.loc, 'r') as file:
            jsonString = file.read().replace('\n', '')

        self.myDict = json.loads(jsonString)

    def updateFile(self):
        with open(self.loc, 'w') as x:
            x.write(json.dumps(self.myDict))

    def create(self, key : str, val : str, timer = -1):
        '''
            Create a key-value pair

            optional parameter : 
                timer ->    This parameter is used as timer after those many seconds 
                            the key will be removed from the dictionary
        '''
        if key in self.myDict.keys():
            print("The key exists in the database")

        else:
            if key.isalpha():
                if len(key) <= 32 and len(self.myDict) < 1024*1024*1024 and len(val) <= 16*1024:
                    self.myDict[key] = val
                    self.updateFile()
            if timer != -1:
                threading._start_new_thread(self.running, (key, time.time() + timer, self.lock, ))

    def read(self, key):
        '''
            Reads and displays the the value of the parameter key
        '''
        if key in self.myDict.keys():
            print(f"{key} : {self.myDict[key]}")
        else:
            print("The key does not exists in database")

    def delete(self, key, verbose = True):
        '''
            Displays and deletes the key-value pair of the given key
        '''
        if key in self.myDict.keys():
            if verbose:
                print(f"{key} : {self.myDict[key]}" + " has been deleted")
            self.myDict.pop(key)
            self.updateFile()
        else:
            if verbose:
                print("The key does not exists in database")

    def running(self, key, timer, lock):
        '''
            This method is used to delete the key from the MyDict object after
            'timer' seconds.
        '''
        while time.time() < timer:
            pass
        '''
            The below code is for thread safety
        ''' 
        lock.acquire()
        self.delete(key, False)
        lock.release()

if __name__ == "__main__":
    '''
        Basic code to how to use the functionalities
    '''
    c = CRD()

    while True:

        print('1.Create\n2.Read\n3.Delete\n4.exit')
        x = int(input('Enter choice : '))

        if x == 1:
            key = input('Enter Key : ')
            val = input('Enter JSON String or normal string : ')
            timer = input('Enter timer (-1 for infinite) : ')

            c.create(key, val, float(timer))

        elif x == 2:
            key = input('Enter key : ')
            c.read(key)

        elif x == 3:
            key = input('Enter key : ')
            c.delete(key)

        else:
            break

