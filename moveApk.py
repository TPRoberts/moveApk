#! /usr/bin/python -B

###############################################################
########                  moveApk.py                   ######## 
########             Made by Thomas Roberts            ######## 
########                  14/02/2016                   ########
###############################################################

import os
import sys
import logging
import shutil


# Move Apk function
# Input :- Source DIR
# Input :- Destination DIR
# Output :- None
# Description:- This function will move all *.apk's in one directory 
# and put them in their respective folders
def moveApks(source, destination, move):
    # Return Value initialisations
    returnValue = True

    logging.info("Scanning %s for APK's", source)
    # Scan the sour DIR to find all APK's init
    apks = [f for f in os.listdir(source) if f.endswith('apk')]
    
    if (len(apks) > 0):
        logging.info("Found %d APK's to move", len(apks))
        for i in range(len(apks)):
            # Start moving APK's
            src = os.path.abspath(source + "/" + apks[i])
            destDir = os.path.abspath(destination + "/" +apks[i].replace(".apk", ""))
            dest =  os.path.abspath(destDir + "/" + apks[i])
            if not os.path.isdir(destDir):
                os.mkdir(destDir)

            if move:
                logging.info("Moving %s to %s", src, dest)
                shutil.move(src, dest)
            else:
                logging.info("Copying %s to %s", src, dest)
                shutil.copy(src, dest)
    else:
        # We didn't find any APK's
        logging.error("Found no APK's in %s", source)
        returnValue = False
        
    return returnValue


# Check Arguments
# Input:- Source directory
# Input:- Destination directory
# Output:- Boolean, True is everything is ok
# This function will check the source and destination directory
def checkArgs(source, destination):

    returnValue = True
    
    if not os.path.isdir(source):
        logging.error("Source directory %s doesn't exist", source)
        returnValue = False

    if not os.path.isdir(destination):
        logging.warning("Destination %s doesn't exist", destination)
        logging.info("Making destination directory as it doesn't exists")
        os.makedirs(destination)

    return returnValue

# Yes No Prompt
# Input:- Question
# Input:- default answer (default is yes unless changed)
# Output:- Boolean
# Description :- Prompt the user with a yes no question and return boolean.
def queryYesNo(question, default="yes"):

    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


# Clear shell script
# Input:- None
# Output:- None
# Description: This function will clear the shell 
def cls():
    os.system(['clear','cls'][os.name == 'nt'])

# Main
if __name__ == "__main__":
    
    # Initialise all logging configuration, only levels equal to info or above will be logged, the stream will be stdout and message will appear as the following:
    # DEBUG: This is DEBUG (only if configured)
    # INFO: This is information
    # Warning: This is a warning
    # Error: This is a error
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(levelname)s: %(message)s')

    # Clean the shell
    cls()

    # Check arguments
    if len(sys.argv) > 1:
        if len(sys.argv) < 3 or len(sys.argv) > 4:
            logging.error("*** usage: %s <source directory> <destination directory> <move flag>* \n\n* Optional use '-m' to move APKs instead of copy % sys.argv[0]")
        else:
            if (len(sys.argv) == 4):
                if (sys.argv[3] == "-m"):
                    # Move flag is set
                    if (checkArgs(sys.argv[1], sys.argv[2])):
                        moveApks(sys.argv[1], sys.argv[2], True)
                    else:
                        logging.error("Failed when checking arguments")
                else:
                    logging.warning("Invalid move flag, so we will just copy instead")
                    # Move flag is set
                    if (checkArgs(sys.argv[1], sys.argv[2])):
                        moveApks(sys.argv[1], sys.argv[2], False)
                    else:
                        logging.error("Failed when checking arguments")
            else:
                # Move flag isn't set
                if (checkArgs(sys.argv[1], sys.argv[2])):
                    moveApks(sys.argv[1], sys.argv[2], False)
                else:
                    logging.error("Failed when checking arguments")
    else:
        # We have no arguments pass to use we will prompt the user
        src = raw_input("Please enter a source directory: ")
        dest = raw_input("Please enter a destination directory: ")
        mvOpt = queryYesNo("Would you like to move the APKs instead of copy?")

        if (mvOpt):
            # Move flag is set
            if (checkArgs(src, dest)):
                moveApks(src, dest, True)
            else:
                logging.error("Failed when checking arguments")
        else:
            # Move flag isn't set
            if (checkArgs(src, dest)):
                moveApks(src, dest, False)
            else:
                logging.error("Failed when checking arguments")
    
    end = raw_input("\nDone! Press any key to exit....")