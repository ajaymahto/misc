import datetime
from subprocess import Popen, PIPE

today = datetime.datetime.now()
year = today.year
day_num = getDayNum()

# Function to get the day number
def getDayNum():
  day_of_year = (today - datetime.datetime(year, 1, 1)).days + 1
  return day_of_year

# Function to check if POP is ready
def popReady(path):
    ready = True
    day_num = getDayNum()
    summary = path + "/" + "C030prnSummary" + day_num + "_" + year
    eventlog = path + "/" + "EventLog_" + day_num + "_" + year + ".txt"
    pop_filed1 = path + "/" + "PopFiled1_" + year + "_" + day_num + "_C03"
    pop_filed2 = path + "/" + "PopFiled1_" + year + "_" + day_num + "_C03.pop"
    pop_filed3 = path + "/" + "PopFiled1_" + year + "_" + day_num + "_C03.pri"
    pop_listd = path + "/" + "PopListd1_" + year + "_" + day_num + "_C03.POP"
    time_events_cmds = path + "/" + "TimeEvents1Cmds" + day_num + year + ".dat"
    if not path.exists(summary):
        ready = False
    if not path.exists(eventlog):
        ready = False
    if not path.exists(pop_filed1):
        ready = False
    if not path.exists(pop_filed2):
        ready = False
    if not path.exists(pop_filed3):
        ready = False
    if not path.exists(pop_listd):
        ready = False
    if not path.exists(time_events_cmds):
        ready = False
    return ready

# Generic function to run a bash command from Python
def runCommand(cmd):
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    output, err = p.communicate()
    if err:
        return False
    return True

# Function to run the PlVerify commands
def runPlVerify():
    cmd = "PlVerify.sh" + " " + day_num + " " + year
    return runCommand(cmd)

# Function to run the lpr commands
def runLPR(path):
    summary = path + "/" + "C030prnSummary" + day_num + "_" + year
    pop_filed3 = path + "/" + "PopFiled1_" + year + "_" + day_num + "_C03.pri"
    summary_lpr_cmd = "lpr " + summary
    pop_filed3_lpr_cmd = "lpr" + pop_filed3
    # Run LPR command for line 2: summary file
    if runCommand(summary_lpr_cmd):
        print(summary_lpr_cmd + " FAIL!")
        return False
    # Run LPR command for line 8: pop_filed3 (.pri) file
    if runCommand(pop_filed3_lpr_cmd):
        print(pop_filed3_lpr_cmd + " FAIL!")
        return False

# The Main Function
def main():
    # Input area path from user
    path = input("ENTER AREA PATH: ")
    path = path.rstrip('/')
    # Check if POP is ready
    if popReady(path):
        print("POP READY!")
        # Run PlVerify if POP is ready
        if runPlVerify():
            print("PLVERIFY COMMAND SUCCESS!")
            # Run LPR commands if PLVerify is Success
            if runLPR(path):
                print("LPR COMMANDS SUCCESS!")
            else:
                print("LPR COMMANDS FAIL!")
        else:
            print("PLVERIFY COMMAND FAIL!")
    else:
        print("POP NOT READY!")
