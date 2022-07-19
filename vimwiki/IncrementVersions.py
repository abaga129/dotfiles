{{{py
import os
import sys
import copy
from os import path
import glob
import uuid

incrementMajor = False
incrementMinor = False
incrementPatch = True

class Version:
    Major = ""
    Minor = ""
    Patch = ""
    Build = ""

    def __str__(self):
        return self.Major + "." + self.Minor + "." + self.Patch + ("." + self.Build if self.Build != "" else "")

    def toStringWithoutBuildNumber(self):
        return self.Major + "." + self.Minor + "." + self.Patch

def processLine(line):
    version = Version()

    versionNumber = line.split("\"")[1]
    versionNumberSplit = versionNumber.split(".")

    version.Major = versionNumberSplit[0]
    version.Minor = versionNumberSplit[1]
    version.Patch = versionNumberSplit[2]
    if len(versionNumberSplit) > 3:
        version.Build = versionNumberSplit[3]


    newVersion = copy.copy(version)

    if incrementMajor:
        newVersion.Major = str(int(newVersion.Major) + 1)
        newVersion.Minor = "0"
        newVersion.Patch = "0"

    if incrementMinor:
        newVersion.Minor = str(int(newVersion.Minor) + 1)
        newVersion.Patch = "0"

    if incrementPatch:
        newVersion.Patch = str(int(newVersion.Patch) + 1)

    print(str(version) + " -> " + str(newVersion))

    return str(line).replace(str(version), str(newVersion))

def processProductCodeLine(line):
    # "ProductCode" = "8:{5175405A-E8B4-4502-A53F-3A0289B31850}"
    guid = uuid.uuid4()
    newLine = '        "ProductCode" = "8:{' + str(guid).upper() + '}"\n'
    return newLine

def processProductVersionLine(line):
    # "ProductVersion" = "8:1.8.3"
    version = Version()

    versionNumber = line.split(":")[1]
    versionNumber = versionNumber.split('"')[0]
    versionNumberSplit = versionNumber.split(".")

    version.Major = versionNumberSplit[0]
    version.Minor = versionNumberSplit[1]
    version.Patch = versionNumberSplit[2]
    if len(versionNumberSplit) > 3:
        version.Build = versionNumberSplit[3]

    newVersion = copy.copy(version)

    if incrementMajor:
        newVersion.Major = str(int(newVersion.Major) + 1)
        newVersion.Minor = "0"
        newVersion.Patch = "0"

    if incrementMinor:
        newVersion.Minor = str(int(newVersion.Minor) + 1)
        newVersion.Patch = "0"

    if incrementPatch:
        newVersion.Patch = str(int(newVersion.Patch) + 1)

    newLine = '        "ProductVersion" = "8:' + version.toStringWithoutBuildNumber() + '"\n'
    return newLine

def fileReplace(file, oldString, newString):
    for line in file:
        file.write(line.replace(oldString, newString))

def incrementVersionForFile(folder, filePath, fileTempPath):
    if path.exists(filePath):
        print(folder + " Contains a .NET Project")
        propertiesFile = open(filePath, "r")
        propertiesFileTemp = open(fileTempPath, "a+")

        for line in propertiesFile.readlines():
            newLine = line
            if ("AssemblyVersion" in line or "AssemblyFileVersion" in line) and not line[0:2] == "//" and not line[0:1] == "'":
                print(newLine.replace('\n', ''))
                newLine = processLine(line)
                propertiesFileTemp.write(newLine)
            else:
                propertiesFileTemp.write(line)

        propertiesFile.close()
        propertiesFileTemp.close()

        os.remove(filePath)
        os.rename(fileTempPath, filePath)
        print()


def incrementSetupProject(folder):
    print("Looking for setup project")
    path = folder + "**/*.vdproj"
    files = glob.glob(path)
    for file in files:
        fileTempPath = "temp.vdproj"
        print("Found Setup Project File: " + file)
        projectFile = open(file, "r")
        projectFileTemp = open(fileTempPath, "a+")

        for line in projectFile.readlines():
            newLine = line
            if ('        "ProductCode" = "8:' in line and not 'ProductCode" = "8:.' in line):
                print(newLine.replace('\n', ''))
                newLine = processProductCodeLine(line)
                projectFileTemp.write(newLine)
            elif ("""ProductVersion""" in line):
                print(newLine.replace('\n', ''))
                newLine = processProductVersionLine(line)
                projectFileTemp.write(newLine)
            else:
                projectFileTemp.write(line)

        projectFile.close()
        projectFileTemp.close()

        os.remove(file)
        os.rename(fileTempPath, file)

def main():
    global incrementMajor, incrementPatch, incrementMinor
    for index, arg in enumerate(sys.argv):
        if arg == "--major":
            incrementMajor = True
            incrementPatch = False
        if arg == "--minor":
            incrementMinor = True
            incrementPatch = False
        if arg == "--dir":
            os.chdir(sys.argv[index + 1])
        if arg == "--help" or arg == "-h" or arg == "--h":
            help()
            exit

    projectFolders = [ f.path for f in os.scandir("./") if f.is_dir() ]

    for folder in projectFolders:

        csharpAssemblyInfoPath = folder + "/Properties/AssemblyInfo.cs"
        csharpAssemblyInfoPathTemp = folder + "/Properties/AssemblyInfo-temp.cs"
        incrementVersionForFile(folder, csharpAssemblyInfoPath, csharpAssemblyInfoPathTemp)

        vbAssemblyInfoPath = folder + "/My Project/AssemblyInfo.vb"
        vbAssemblyInfoPathTemp = folder + "/My Project/AssemblyInfo-temp.vb"
        incrementVersionForFile(folder, vbAssemblyInfoPath, vbAssemblyInfoPathTemp)

    incrementSetupProject("./")

    finished_message()

def help():
    print ("Usage: python increment-versions.py --dir <project_path> --major --minor --patch")

def finished_message():
    print ("All C# and Visual Basic projects have been incremented.\n\nIf the project contains a Setup Project, be sure to increment the version manually in it.")

main()%
}}}
