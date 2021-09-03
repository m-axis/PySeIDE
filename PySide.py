import json
import os
import sys
import yaml

folderName = sys.path[0]
testConfig = {}
print('Extrating Test Config.....')
with open(f'{folderName}\\TestConfig.yaml') as f:
        testConfig = yaml.load(f, Loader=yaml.FullLoader)
print('Test Config loaded.')

sideFileName = testConfig['source_file_name']
sampleFileName = testConfig['sample_file_name']
newFolderName = sideFileName.split(".")[0]
print(newFolderName)
print('Loading Source file.....')
foldersToCreate = [f'{folderName}\\{newFolderName}', f'{folderName}\\{newFolderName}\\testsJSONS', f'{folderName}\\{newFolderName}\\suites']
PROJECT_DIR = foldersToCreate[0]
TESTS_DIR = foldersToCreate[1]
EXTRACTED_PROJECT_DIR = foldersToCreate[2]
sourceFile = open(os.path.join(folderName, sideFileName), "r")
sourceText = sourceFile.read()
sourceJSON = json.loads(sourceText)
sourceFile.close()
tests = sourceJSON["tests"]
suites = sourceJSON["suites"]
print('Source file loaded.')

commandsFromTests = {}
  

for folder in foldersToCreate:
    if not os.path.exists(folder):
        os.makedirs(folder) 

#converting tests into JSON files
print('Converting tests into JSON files.....')
for test in tests:
    fileName = test["name"]
    if testConfig["create_json"]:
        with open(f'{TESTS_DIR}\\{fileName}.json', 'w') as testFile:
            testFile.write(str(test))
    commandsFromTests[test["id"]] = test["commands"]
print('Tests converted into JSON files successfully.')

#converting Suites to tests using commands
print('Converting Suites to tests.....')
sampleProject =  open(os.path.join(folderName, sampleFileName), "r")
sampleProjectJSON = json.loads(sampleProject.read())
tcCount = 0
for suite in suites:  
    tcCount += 1 
    extractedCombinedTests = {}                                                                                                                                 
    extractedCombinedTests["id"] = suite["id"]    
    extractedCombinedTests["name"] = f"TC_{tcCount}_" + suite["name"]
    extractedCombinedTests["commands"]  = [] 
    #Converting tests into commands in order to convert suite into a sinle test
    for testId in suite["tests"]:
        extractedCombinedTests["commands"] += commandsFromTests[testId]
    sampleProjectJSON["tests"].append(extractedCombinedTests)
    sampleProjectJSON["suites"][0]["tests"].append(suite["id"])
print('Converted suites to tests.')

print('Creating New project file using the sample provided.....')
sampleProjectJSON["url"] = testConfig["url"]  
sampleProjectJSON["urls"] = sourceJSON["urls"]    
sampleProjectJSON["plugins"] = sourceJSON["plugins"]  
sampleProjectJSON["name"] = sourceJSON["name"] + "_Extracted"
targetFileName = f"Extracted_{sideFileName}"
with open(f"{EXTRACTED_PROJECT_DIR}\\{targetFileName}", "w") as targetFile:
    targetFile.write(json.dumps(sampleProjectJSON))
print('Successfully created the project file.')
print('Ready to start the test now.')
