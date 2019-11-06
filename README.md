# mat2obj
Loads .mat MatLab files in Python in a similar syntax to MatLab's.   
      
# Prerequisites:
python3       
python modules:     
+ numpy     
+ scipy     
     
# How to run:
`import mat2obj`   
`myMat=mat2obj.filename('filename')`   
      
# How to use output:
`myMat.DWI`   
`myMat.DWI.hdr`   
`myMat.DWI.dat`    
`myMat.DWI.dat[3][2][5]` #assumming dat is a 3D matrix     
`myMat.DWI.hdr.private`     
       
# How to get options (available paths) (in list format):
`mat2obj.options(matobj)`
       
## Examples for running mat2obj.options (input is of type <class 'mat2obj.Struct'>):       
`mat2obj.options(myMat)`     
`mat2obj.options(myMat.DWI)`   
`mat2obj.options(myMat.DWI.hdr)`   
`mat2obj.options(myMat.DWI.hdr.private)`   

# Extra (.mat to dictionary):
`myDict=mat2obj.loadmat('filename')` 
