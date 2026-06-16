
"""
Open Panoptes (API Key for Zooniverse) and search for the Burst Chaser project.
This links to the source of all light curve images and data.

SUMMARY OF FILE:
This file defines the classes and methods used for Burst Chaser project. It is responsible for 
creating instances of bursts, categorizing them by their pulse shape and follow-up pulses,
distinguishing between pulse and noise, and locating/counting pulses. It also includes methods
for exporting the classifications and locations to csv files for further analysis. 
"""

import pandas as pd # used to read the csv file and create data frames
import os # used to find the png files in the folder

count = 0 # count of verified bursts - used to retire subjects after 20 classifications

# Parent Class - responsible for general burst properties
class BurstChaser():
    # Constructor
    def __init__(self, Burst_Name, Burst_ID, workflow, verify = None):
        self.Burst_Name = Burst_Name
        self.Burst_ID = Burst_ID
        self.workflow = workflow
        self.verify = verify
        self.contributors = []
        
    # Getters
    @property
    def Burst_Name(self):
        return self._Burst_Name
    @property
    def Burst_ID(self):
        return self._Burst_ID
    @property
    def workflow(self):
        return self._workflow
    @property
    def verify(self):
        return self._verify 
    @property
    def contributors(self):
        return self._contributors 

    # Setters
    @Burst_Name.setter
    def Burst_Name(self, n):
        self._Burst_Name = n    
    @Burst_ID.setter
    def Burst_ID(self, i):
        self._Burst_ID = i
    @workflow.setter
    def workflow(self, w):
        self._workflow = w
    @verify.setter
    def verify(self, v):
        self._verify = v
    @contributors.setter
    def contributors(self, c):
        self._contributors = c
    
    # Deleters
    #     workflow = Workflow.find(f"{self.workflow}")
    #     workflow.retire_subjects(f"{self.BurstID}")
      
    # Instance Methods:
    # => Retires a subject and verify the burst
    def retire(self):
        global count
        if self.verify != None:
            count += 1
           
    # => Adds contributors
    def contributorsAdd(self, ct):
        self.contributors.append(ct)

    # Static Method: 
    # => Searches BurstPhotos for corresponding png file name and return it
    @staticmethod
    def findPNG(name, path="BurstPhotos"):
        for filename in os.listdir(path):
            if name in filename and os.path.isfile(os.path.join(path, filename)):
                return filename #return path and file name os.path.join(path, filename)
        return "None"

    # Dunder Method:
    # => Compares two bursts by their ID number for sorting purposes
    def __lt__(self, other):
        return self.Burst_ID < other.Burst_ID

# Child Class - responsible for ranking all the bursts and categorizing them by their pulse shape and follow-up pulses 
class PulseShape(BurstChaser):
    # Constructor
    def __init__(self, Burst_Name, Burst_ID, workflow):
        super().__init__(Burst_Name, Burst_ID, workflow)
        self.Shape = [0,0,0,0]
        self.Follow = [0,0,0,0,0,0]
    
    # Getters
    @property
    def Shape(self):
        return self._Shape
    @property
    def Follow(self):
        return self._Follow
    
    # Setters
    @Shape.setter
    def Shape(self, s):
        self._Shape = s 
    @Follow.setter
    def Follow(self, f):
        self._Follow = f

    # Dunder Methods:
    # => String representation of the burst and its properties
    def __str__(self):
        #return f"{self.BurstID}:  Simple:{self.Shape[0]}  Ext:{self.Shape[1]}  Other:{self.Shape[2]} Follow Up:{self.Follow}"
        return f"{self.Burst_ID}:  Shape:{self.Shape}  Follow Up:{self.Follow} Verified:{self.verify}"

    # Instance Methods:
    # => Counts the number of times a burst is classified with a certain pulse shape
    def ShapeCount(self, shape):
        if "extended emission" in shape:
            self.Shape[1] += 1
        elif "simple pulse" in shape:
            self.Shape[0] += 1
        elif "other" in shape:
            self.Shape[2] +=1
        elif "too noisy" in shape:
            self.Shape[3] +=1

     # => Counts the number of times a burst has follow-up pulses with certain properties
    def FollowCount(self, j):
        if 'Pulses connected with underlying emission.' in j: 
            self.Follow[2] += 1
        if 'Symmetrical structure' in j:
            self.Follow[0] += 1
        if "One or more pulses with the fast-rise and slow-decay shape." in j:
            self.Follow[1] += 1
        if 'Rapid varying pulses' in j:
            self.Follow[3] += 1
        if "I don't see any of these" in j:
            self.Follow[4] += 1
        if "Too noisy" in j:
            self.Follow[5] += 1

    # => Exports the counts of pulse shapes and follow-up pulses to a csv file
    def export(name, pulse_list):
        pulse_list = sorted(pulse_list)
        data = {'Burst_Name': [i.Burst_Name for i in pulse_list],
                'Burst_PNG': [PulseShape.findPNG(i.Burst_Name) for i in pulse_list],
                'Simple': [i.Shape[0] for i in pulse_list],
                'Extended': [i.Shape[1] for i in pulse_list],
                'Other': [i.Shape[2] for i in pulse_list],
                'Too_Noisy': [i.Shape[3] for i in pulse_list],
                'Follow': [i.Follow for i in pulse_list]
                }
        # Converts raw data into a data frame for easier export to csv file
        df = pd.DataFrame(data)
        df.to_csv(f'CSVExports/{name}.csv', index = False, header = True)

# Child Class - responsible for distinguishing between the pulse and noise
class PulseNoise(BurstChaser):
    def __init__(self, Burst_Name, Burst_ID, workflow):
        super().__init__(Burst_Name, Burst_ID, workflow)
        self.classification = [0,0,0,0]
        
    # Getter
    @property
    def classification(self):
        return self._classification

    # Setter  
    @classification.setter
    def classification(self, c):
        self._classification = c
        
    # Instance Methods:
    # => Count the number of times a burst is classified as a pulse or other categories
    def classCount(self, a):
        if "This is a pulse." in a:
            self.classification[0] += 1
        elif "This is noise." in a:
            self.classification[1] += 1
        elif "It's hard to tell." in a: 
            self.classification[2] += 1
        else:
            self.classification[3] += 1

    # => Exports the PulseNoise classifications to a csv file
    def export( name, pulse_list):
        pulse_list = sorted(pulse_list)
        data = {'Burst Name': [i.Burst_Name for i in pulse_list],
                'Burst ID': [i.Burst_ID for i in pulse_list],
                'Pulse': [i.classification[0] for i in pulse_list],
                "Noise": [i.classification[1] for i in pulse_list],
                'Cant Tell': [i.classification[2] for i in pulse_list],
                'No Response': [i.classification[3] for i in pulse_list]
                }
        # Converts raw data into a data frame for easier export to csv file
        df = pd.DataFrame(data)
        df.to_csv(f'CSVExports/{name}.csv', index = True, header = True)

    # Dunder Method:
    # => Returns a string representation of the classification
    def __str__(self):
        return f"{self.Burst_ID}: Classification: {self.classification}"

# Child Class - responsible for the locating and counting pulses
class PulseLocation(BurstChaser):
    def __init__(self, Burst_Name, Burst_ID, workflow):
        super().__init__(Burst_Name, Burst_ID, workflow)
        self.locations =  []
        self.count = 0 

    # Getters
    @property
    def count(self):
        return self._count
    @property
    def locations(self):
        return self._locations
    
    # Setters
    @count.setter
    def count(self ,i):
        self._count = i
    @locations.setter
    def locations(self, i):
        self._locations = i

    # Instance Methods:
    # => Reads the location of the pulse from the classification and adds it to the list of locations
    def read(self, a):
        a = a.split(' which is automatically determined by a computer algorithm.","value":[')[1]
        self._count += 1
        if '},{' in a:
            a = a.split('},{')
        else:
            a = [a]
        for i in a:
            cata = i.split(",")
            print(cata)
            if len(cata) > 4:
                # Correction
                loc = Location(float(cata[0].split(":")[1]), float(cata[1].split(":")[1]), float(cata[4].split(":")[1]), float(cata[5].split(":")[1]))
                self.locations.append(loc)

    # => Finds the GRB name from the Subject ID number
    def findGRB(self, sid):
        file = pd.read_csv("GRB_IDS_Names.csv")
        file.set_index('Subject_ID', inplace=True)
        return file.loc[sid,'GRB_Names']
               
    # => Exports the pulse locations to a csv file      
    def export(name, pulse_list):
        Burst_Name = []
        Burst_ID =[]
        x = []
        y = []
        h = [] 
        w = []
        
        for i in sorted(pulse_list):
            if len(i.locations) != 0:
                Burst_Name.append(i.Burst_Name)
                Burst_ID.append(i.Burst_ID)
                tempx = []
                tempy = []
                temph = []
                tempw = []
                for j in i.locations:
                    tempx.append(j.x)
                    tempy.append(j.y)
                    tempw.append(j.width)
                    temph.append(j.height)
                x.append(tempx)
                y.append(tempy)
                h.append(temph)
                w.append(tempw)
        print(len(x))
        print(len(Burst_Name))
        
        data = {'Burst Name': Burst_Name,
                # 'Burst ID': Burst_ID,
                'X_Locations': x,
                'Y_Locations': y,
                'Heights': h,
                'Widths': w
                }
        # Converts raw data into a data frame for easier export to csv file
        df = pd.DataFrame(data)
        df.to_csv(f'CSVExports/{name}.csv', index = True, header = True)
        
# Parent Class - responsible for location properties of the pulse
class Location():
    # Constructor
    def __init__(self, x=0, y=0, height=0, width=0):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
    
    # Getters
    @property
    def x(self):
        return self._x
    @property
    def y(self):
        return self._y
    @property
    def height(self):
        return self._height
    @property
    def width(self):
        return self._width
    
    # Setters
    @x.setter
    def x(self, i):
        self._x = i
    @y.setter
    def y(self, i):
        self._y = i   
    @height.setter
    def height(self, i):
        self._height = i
    @width.setter
    def width(self, i):
        self._width = i

    # The japanese wife that I met online and I are hitting it off pretty well and let me tell you, i am so in love with her. Im moving next week. WOW!