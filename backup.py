# Import the following modules
import shutil
import os
import sys
import sched
import time
import cProfile
from datetime import date, datetime, timedelta
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
import glob
import pathlib
from operator import add


#global variables
source = r"C:\String\here"
destination = r"\\server\string\here"

#Search newest file by n day and send the complete string to be copied 
def findNew(well,day=0):
        fname = pathlib.Path(well)
        last = fname.stat().st_mtime
        timeStamp = datetime.fromtimestamp(last)
        referencia = datetime.today() - timedelta(days=day)
        logging.debug('modificacion: ',timeStamp,'\nReferencia: ',referencia)
        if timeStamp>referencia:
            return well
        else:
            return []

### Function for performing the backup of the files and folders
def copy_file(ss,d,dia):
    c = 0
    welp = glob.glob(ss+"\\*.*")
    if welp == []:
        logging.info("No se encontro el directorio")
    else:
        #print(welp)
        for w in welp:
            copyco = findNew(w,dia)
            #print("Esto es lo que se va a copiar: ",type(copyco))
            if copyco != []:
                try:
                    logging.info("Archivo a copiar:\n",copyco)
                    shutil.copy2(copyco, d)
                    logging.info("se copio informacion")
                except FileNotFoundError:
                    print("File does not exists!,\
                        please give the complete path")
            c = c + 1
    log = str('EVENT:' + time.ctime(int(time.time())))
    logging.info(log)
    


#PROGRAM START
filename = 'stats.log'
pathe = os.path.join(destination, filename)

logging.basicConfig(filename=pathe, encoding='utf-8', level=logging.DEBUG)
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

# instance is created
scheduler = sched.scheduler(time.time,time.sleep)
#---------------------

src = [source] * 4
dstt = [destination] * 4

## need to fill for specific folders 
folders_name_s = ["name","of","specific","folders"]
folders_name_D = ["name","of","specific","folders"]

sr = []
dst = []

rr = range(4)
for d in rr:
   srPath = os.path.join(src[d],folders_name_s[d])
   dstPath = os.path.join(dstt[d],folders_name_D[d])
   sr.append(srPath)
   dst.append(dstPath)

# printing starting time
logg = str('START:' + date.today().strftime("%d_%b_%Y_"))
logging.info(logg)

scheduler = BlockingScheduler()

### Copy from folder 1, every 5 min
scheduler.add_job(copy_file, 'cron', args=[sr[0],dst[0],1],minute='*/30',second=2,name="Copia Folder 1")

### Copy from folder 2, 3 times a day 1:05, 7:05, 16:05 
scheduler.add_job(copy_file, 'cron', args=[sr[1],dst[1],7], hour=1, minute=5,second=4,name="Copia folder 2, 1:05 am")
scheduler.add_job(copy_file, 'cron', args=[sr[1],dst[1],7], hour=7, minute=5,second=4,name="Copia folder 2, 7:05 am")
scheduler.add_job(copy_file, 'cron', args=[sr[1],dst[1],7], hour=16, minute=35,second=4,name="Copia folder 2, 16:05 am")

### Copy from folder 3 times a day 1:05, 7:05, 16:05 
scheduler.add_job(copy_file, 'cron', args=[sr[2],dst[2],1], hour=1, minute=5,second=3,name="Copia folder 3, 1:05 am")
scheduler.add_job(copy_file, 'cron', args=[sr[2],dst[2],1], hour=7, minute=5,second=3,name="Copia folder 3, 7:05 am")
scheduler.add_job(copy_file, 'cron', args=[sr[2],dst[2],1], hour=16, minute=35,second=3,name="Copia folder 3, 16:05 am")

### Copy from foler 4 every 30 min
scheduler.add_job(copy_file, 'cron', args=[sr[3],dst[3],7],minute='*/30',second=0,name="Copia folder 4")

try:
    scheduler.start()

        
except:
    logging.error("Scheduling failure")
