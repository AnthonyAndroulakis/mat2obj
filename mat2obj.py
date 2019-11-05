#mat2obj.py
#How to run:
#import mat2obj
#mat2obj.filename('filename')
#
#How to convert mat 2 dictionary:
#mat2obj.loadmat('filename')
#
#
# loadmat is from stackoverflow, written by users cs01 and jpapon here:
# https://stackoverflow.com/a/29126361
#
# class Struct is from stackoverflow, written by user andyvanee
# https://stackoverflow.com/a/6573827
#
'''
At any point, you can find which options are available by setting a variable called matobj to your object IN QUOTATIONS and running the command below:
list(eval('{key: value for key, value in '+matobj+'.__dict__.items() if not key.startswith("__") and not key.startswith("_")}.keys()'))

Examples for defining matobj include but are definitely not limited to:
matobj="patient"
matobj="patient.DWI"
matobj="patient.DWI.hdr"
matobj="patient.DWI.hdr.private"
'''


import scipy.io as spio
import scipy.io
import numpy as np

class Struct:
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

def loadmat(filename):
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

def filename(file):
    if file[-4:]=='.mat':
      loadoutput=loadmat(file)
      structoutput=Struct(loadoutput)
      return structoutput
    else:
      print('Only .mat files are accepted.')
