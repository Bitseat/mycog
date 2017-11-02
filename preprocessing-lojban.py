import os
import sys
import fileinput
import re
import linecache

fileToSearch  = "/home/bitseat/Documents/oct28/replaceResult.scm"

someFile = open( fileToSearch, 'r+' )
tempFile = open ("bit.txt", 'w')
newFile = open ("replaceResult.scm", 'w')


pattern = r'"([A-Za-z0-9_\./\\-]*)"'
 
tempFile.writelines([l for l in open("/home/bitseat/Documents/oct28/replaceResult.scm").readlines()])     
print "made bit"
tempFile.close()

tempFile = open ("bit.txt", 'r+')

def findReplacment (org_string):
    #find a subsetLink that has a conceptNode with org_string, go lower into its EvaluationLink and find the predicateNode
    inSubset = False
    inSatisfyingScope = False
    inEvalListLink = False
    tempFile = open ("bit.txt", 'r+')
        
    for line in tempFile:
         if "SubsetLink" in line:
              inSubset = True
         if inSubset and "ConceptNode" in line:
              val = re.search(pattern, line)  
              if(val is not None):
                  val = str(val.group())
                  if (val == org_string): 
                      continue
                  else:    
                      inSubset = False
         if inSubset and "SatisfyingSetScopeLink" in line:
                    inSatisfyingScope = True            
         if inSatisfyingScope and "ListLink" in line:
              inEvalListLink = True
         if "Link" in line and not "SatisfyingSetScope" in line and not "Evaluation" in line and not "List" in line and not inSubset:
              # we have gone outside of the SubsetLink parameters
              inSubset = False
              inSatisfyingScope = False
              inEvalListLink = False      
         if inEvalListLink and "PredicateNode" in line:
              val = re.search(pattern, line)  
              if(val is not None):
                  print "\n"+val.group()+"\n"
                  val = str(val.group())
                  print "replacment word is"+val
                  tempFile.close()
                  return val
    tempFile.close()
    return ""                        
           

inEval = False
inEvalList = False
count = 0
for line in someFile:
      count +=1
      if "EvaluationLink" in line : 
          inEval= True 
          #print "inEval!"
      if (inEval and "ListLink" in line):           
          inEvalList = True
          #print "inEvalLink"
      if (inEval and "Link" in line and not "List" in line and not "Evaluation" in line):  
           #print "removing"  
           inEval = False
           inEvalList = False          
      if (inEvalList and "ConceptNode" in line): 
          
          val = re.search(pattern, line)
          if(val is not None):
             print "\n"+val.group()+"\n"
             val = str(val.group())
             print val
             if(val.endswith('___"')):
                 textToReplace = findReplacment(val)
                 if textToReplace == "":
                     print "unreplaced at line" + str(count)
                 elif val in line and not textToReplace == "":
                    print"found val"
                    print line
                    print line.replace (val,textToReplace)
                    newFile.write(line.replace(val, textToReplace))
                    continue;
       
      newFile.write(line)          
    
      
someFile.close()          
newFile.close()  
os.remove('bit.txt')        
