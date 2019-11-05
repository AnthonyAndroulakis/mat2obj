# mat2obj
Loads .mat MatLab files in a similar syntax to MatLab's.   
      
# How to run:
`import mat2obj`   
`myMat=mat2obj.filename('filename')`   
      
# How to use:
`myMat.DWI`   
`myMat.DWI.hdr`   
`myMat.DWI.dat`    
`myMat.DWI.dat\[3]\[2]\[5]` #assumming dat is a 3D matrix     
`myMat.DWI.hdr.private`     
       
# How to get options:
set a variable called matobj equal to your object IN QUOTATIONS and run the command below:         
`list(eval('{key: value for key, value in '+matobj+'.\__dict__.items() if not key.startswith("\__") and not key.startswith("\_")}.keys()'))`
       
Examples for defining matobj include but are definitely not limited to:       
`matobj="patient"`     
`matobj="patient.DWI"`   
`matobj="patient.DWI.hdr"`   
`matobj="patient.DWI.hdr.private"`   
