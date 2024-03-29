#mat2obj.py, wrote 2 functions, found 1 function & 1 class on stackoverflow, read below for sources, 2019
#How to run:
#import mat2obj
#mat2obj.filename('filename')
#
#How to convert mat to dictionary:
#mat2obj.loadmat('filename')
#
#
# function loadmat is from stackoverflow, written by users cs01 and jpapon:
# https://stackoverflow.com/a/29126361
#
# class Struct is from stackoverflow, written by user andyvanee
# https://stackoverflow.com/a/6573827
#
# I've writted function filename to combine function loadmat and class Struct.
# I've also written function option so you can see which options/paths your object has. Example run: options(myMat.DWI.hdr)
# Output of function option will be a list of your options. Example: ['fname', 'dim', 'dt', 'pinfo', 'mat', 'n', 'descrip', 'private']

import scipy.io as spio
import scipy.io
import numpy as np

class Struct: #written by user andyvanee (https://stackoverflow.com/a/6573827)
  '''The recursive class for building and representing objects with.'''
  def __init__(self, obj):
    for k, v in obj.items():
      if isinstance(v, dict):
        setattr(self, k, Struct(v))
      else:
        setattr(self, k, v)
  def __getitem__(self, val):
    return self.__dict__[val]
  def __repr__(self):
    return '{%s}' % str(', '.join('%s : %s' % (k, repr(v)) for
      (k, v) in self.__dict__.items()))

def loadmat(filename): #written by users cs01 and jpapon (https://stackoverflow.com/a/29126361)
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    def _check_keys(d):
        '''
        checks if entries in dictionary are mat-objects. If yes
        todict is called to change them to nested dictionaries
        '''
        for key in d:
            if isinstance(d[key], spio.matlab.mio5_params.mat_struct):
                d[key] = _todict(d[key])
        return d

    def _todict(matobj):
        '''
        A recursive function which constructs from matobjects nested dictionaries
        '''
        d = {}
        for strg in matobj._fieldnames:
            elem = matobj.__dict__[strg]
            if isinstance(elem, spio.matlab.mio5_params.mat_struct):
                d[strg] = _todict(elem)
            elif isinstance(elem, np.ndarray):
                d[strg] = _tolist(elem)
            else:
                d[strg] = elem
        return d

    def _tolist(ndarray):
        '''
        A recursive function which constructs lists from cellarrays
        (which are loaded as numpy ndarrays), recursing into the elements
        if they contain matobjects.
        '''
        elem_list = []
        for sub_elem in ndarray:
            if isinstance(sub_elem, spio.matlab.mio5_params.mat_struct):
                elem_list.append(_todict(sub_elem))
            elif isinstance(sub_elem, np.ndarray):
                elem_list.append(_tolist(sub_elem))
            else:
                elem_list.append(sub_elem)
        return elem_list
    data = scipy.io.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)

def filename(file): #combines function loadmat and class Struct, I wrote this
    if file[-4:]=='.mat':
      loadoutput=loadmat(file)
      structoutput=Struct(loadoutput)
      return structoutput
    else:
      print('Only .mat files are accepted.')

def options(matobj): #find options of object, input is your object of type <class 'mat2obj.Struct'>, I wrote this
    try:
        dictmatobj=dict(zip(matobj.__dict__, map(str, matobj.__dict__.values())))
        return list(eval('{key: value for key, value in '+str(dictmatobj)+".items()"+' if not key.startswith("__") and not key.startswith("_")}.keys()'))
    except:
        print("Incorrect type. Correct input type is of <class 'mat2obj.Struct'>.")
