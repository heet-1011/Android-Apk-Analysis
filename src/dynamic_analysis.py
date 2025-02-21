import os 
import logging
from datetime import datetime
import subprocess
from androguard.core.bytecodes import apk
import time
import frida

apiFile = ""

def build_monitor_script(dir, topdown = True):
    script = open("android-trace.js").read()
    return script 


def on_message(message, data):
    with open(apiFile,"a",encoding="utf-8") as file:
        file.write(str(message))


def startAnalysis(fileName, apkName, inputFolder, outputFolder):
    try:
        #=========globals=========
        avdName = "device"
        snapshotName = "default_boot"
        monkeyEvents = 300
        global apiFile
        apiFile = os.path.join(outputFolder,"apicalls/api_calls_"+fileName)

        #=========start log=========
        startTime = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        startTimeDifference = datetime.now()
        print("===============Starting Scan at: "+startTime+"===============")
        logging.info("===============Starting Scan at: "+startTime+"===============")

        #=========api monitor list=========
        apiList = []
        with open("apilist.txt","r") as file:
            for line in file.readlines():
                apiList.append(line.strip("\n"))

        #=========run the emulator=========
        networkFolder = os.path.join(outputFolder,'network',fileName)
        avdCommand = 'emulator -port 5554 -avd '+avdName+' -snapshot '+snapshotName+ ' -no-window -tcpdump "'+networkFolder+'cap"'
        avdProcess = subprocess.Popen(avdCommand,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)     

        #=========adb run=========
        print("Waiting for device...")
        try:
            wait1 = subprocess.Popen("adb -s emulator-5554 wait-for-device",shell=True)
            wait1.wait(timeout=60)
        except:
            print("Fail to up device")
            subprocess.call("ps aux | grep emulator | grep -v grep | awk '{print $2}' | xargs kill -9", shell=True)
            return
        print("Device connected to ADB")

        #=========install app=========
        # path_to_platfrom-tools = os.path.expandvars("$HOME")
        install = subprocess.Popen('adb -s emulator-5554 install '+os.path.join(inputFolder,apkName), shell=True)
        install.wait(timeout=60)
        installCode = install.returncode
        if installCode == 0:
            print("Apk "+ apkName +" installation completed...")

        else:
            subprocess.call("Taskkill /IM "+str(avdProcess.pid)+" /F /T")
            avdProcess.terminate()
            print("Install error")
            return

        #=========get package name=========
        a = apk.APK(os.path.join(inputFolder,apkName))
        package = a.package
        
        subprocess.run('''adb shell su -c "setenforce 0"''', shell=True) 
        addFrida = subprocess.run('''adb -s emulator-5554 push frida-server /data/local/tmp/''', shell=True)
        permissionFrida = subprocess.run('''adb -s emulator-5554 shell "chmod 777 /data/local/tmp/frida-server"''',shell=True)
        apiProcess = subprocess.Popen('''adb -s emulator-5554 shell su -c "/data/local/tmp/frida-server &"''', shell=True)

        time.sleep(30)
        pid = None
        device = None
        session = None
        connected = False
        print("Frida server started...")
        while connected == False:
            try:
                device = frida.get_device("emulator-5554")
                pid = device.spawn(package)
                connected=True
                session = device.attach(pid)
                
            except Exception as e:
                print("[ERROR]: %s" % str(e))
                if str(e) == "unable to connect to remote frida-server: closed":
                    print("Server Reconnect")
                else:
                    subprocess.call("Taskkill /IM "+str(apiProcess.pid)+" /F /T")
                    apiProcess.terminate()
                    subprocess.call("Taskkill /IM "+str(avdProcess.pid)+" /F /T")
                    avdProcess.terminate()
                    return
        
        print("Succesfully Attached to app")
        script_dir = os.path.join(".")
        script_content = build_monitor_script(script_dir)
        script = session.create_script(script_content)  
        script.on("message", on_message)
        script.load()
        script.post({'type': 'tag2', 'payload': apiList})
        device.resume(pid)
        time.sleep(5)

        #=========start strace if want to after getting PID=========
        addstrace = subprocess.run('''adb -s emulator-5554 push strace /data/local/tmp/strace''', shell=True)
        permissionStrace = subprocess.run('''adb -s emulator-5554 shell "chmod 777 /data/local/tmp/strace"''',shell=True)
        straceCommand = "adb -s emulator-5554 shell su -c '/data/local/tmp/strace -p "+str(pid)+" -f -o /data/local/tmp/syscall.txt'"
        straceProcess = subprocess.Popen(straceCommand, shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        #=========wait for app to start=========
        fileLoc = os.path.join(inputFolder,apkName)
        fileSize = os.stat(fileLoc).st_size / (1024 * 1024)
        if fileSize <= 10:
            appStart = 10
        elif fileSize <= 21:
            appStart = 20
        elif fileSize <= 31:
            appStart = 30
        else:
            appStart = 40   

        print("Wait "+str(appStart)+" for app to start. File Size: "+str(fileSize))
        time.sleep(appStart)

        #=========run monkey=========
        print("Starting monkey events")
        try:
            appRun = subprocess.Popen("adb -s emulator-5554 shell su -c 'monkey --throttle 1000 -p "+package+" "+str(monkeyEvents)+"'",shell=True)
        except:
            print("Timedout monkey")
        time.sleep(60)
        #=========save strace=========
        try:
            straceLog = subprocess.Popen('adb -s emulator-5554 pull /data/local/tmp/syscall.txt '+outputFolder+'/systemcalls/',shell=True)
            straceLog.wait(timeout=30)
            print("getting id")
        except Exception as e:
            print("Log timeout")
            subprocess.call("Taskkill /IM "+str(straceProcess.pid)+" /F /T")
            straceProcess.terminate()
            subprocess.call("Taskkill /IM "+str(apiProcess.pid)+" /F /T")
            apiProcess.terminate()
            subprocess.call("Taskkill /IM "+str(appRun.pid)+" /F /T")
            appRun.terminate()
            subprocess.call("Taskkill /IM "+str(avdProcess.pid)+" /F /T")
            avdProcess.terminate()
            print("[ERROR]: %s" % str(e))
            subprocess.call("Taskkill /IM "+str(straceLog.pid)+" /F /T")
            straceLog.terminate()
            return

        endTime = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        print("===============Scan Ended at: "+endTime+"===============\n\n")
        logging.info("===============Scan Ended at: "+endTime+"===============")
        endTimeDifference = datetime.now()
        totalTime = endTimeDifference - startTimeDifference
        print("Total Scan Time: "+ str(totalTime))		
        logging.info("Total Scan Time: "+ str(totalTime))
    except Exception as e:
        subprocess.call("ps aux | grep emulator | grep -v grep | awk '{print $2}' | xargs kill -9",shell=True)
        print(e)
    
    
outputFolder = os.path.expandvars("$HOME/Downloads/dynamic_analysis")
#=========create folders=========

if not os.path.exists(outputFolder):
    print("Output folder not present...Creating Folder")
    logging.info("Output folder not present...Creating Folder")
    os.makedirs(outputFolder)
    print("Output Folder Created\n\n")
    logging.info("Output Folder Created")
if not os.path.exists(outputFolder+"/systemcalls/"):
    print("SystemCalls folder not present...Creating Folder")
    logging.info("SystemCalls folder not present...Creating Folder")
    os.makedirs(outputFolder+"/systemcalls/")
    print("SystemCalls Folder Created\n\n")
    logging.info("SystemCalls Folder Created")
if not os.path.exists(outputFolder+"/network/"): 
    print("Network folder not present...Creating Folder")
    logging.info("Network folder not present...Creating Folder")
    os.makedirs(outputFolder+"/network/")
    print("Network Folder Created\n\n")
    logging.info("Network Folder Created")
if not os.path.exists(outputFolder+"/apicalls/"):
    print("API folder not present...Creating Folder")
    logging.info("API folder not present...Creating Folder")
    os.makedirs(outputFolder+"/apicalls/")
    print("API Folder Created\n\n")
    logging.info("API Folder Created")

loggingDir = outputFolder+"/logs.txt"
logging.basicConfig(filename=loggingDir,format='%(asctime)s %(message)s',level=logging.INFO)

inputFolder = os.path.expandvars("$HOME/Downloads/Android-Apk-Analysis/sample-apks")

for apkName in os.listdir(inputFolder):
    print("Starting Dynamic Analysis for: "+apkName)
    logging.info("Starting Dynamic Analysis for: "+apkName)
    fileName = apkName[:-3]
    startAnalysis(fileName, apkName, inputFolder, outputFolder)
    subprocess.call("ps aux | grep emulator | grep -v grep | awk '{print $2}' | xargs kill -9", shell=True)
    time.sleep(5)