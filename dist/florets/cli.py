import click
import os
import numpy as np
import shutil
import re
from datetime import datetime
import time
import pandas as pd
from colorama import init,Fore,Back,Style
init()

def good(x,r=False):
    if r:
        return Fore.GREEN+Style.BRIGHT+str(x)+Style.RESET_ALL
    else:
        print(Fore.GREEN+Style.BRIGHT+str(x)+Style.RESET_ALL)
    
def inst(x,r=False):
    if r:
        return Fore.CYAN+Style.BRIGHT+str(x)+Style.RESET_ALL
    else:
        print(Fore.CYAN+Style.BRIGHT+str(x)+Style.RESET_ALL)
    
def bad(x,r=False):
    if r:
        return Fore.RED+Style.BRIGHT+str(x)+Style.RESET_ALL
    else:
        print(Fore.RED+Style.BRIGHT+str(x)+Style.RESET_ALL)
    
def question(x,r=False):
    if r:
        return Fore.YELLOW+Style.BRIGHT+str(x)+Style.RESET_ALL
    else:
        print(Fore.YELLOW+Style.BRIGHT+str(x)+Style.RESET_ALL)


reg_format = '(.{5,40})(\.\w{2,5})'

startup_message = "\n\n"+'#'*30+good("\nStarting Floret image Management.",True)+inst("\n--To exit press control C--",True)+"\n"+'#'*30

@click.command()
@click.option('--setup',is_flag=True)
@click.option('--refresh',type=int,default=3,help='How long to wait in seconds before checking again, Default = 3 seconds')
def main(setup,refresh):
    """If a file is in original but not measured or unmeasured, copys it to unmeasured
\nIf a file is in measured and in unmeasured, deletes it from unmeasured"""
    originals_path = ''
    measured_path = ''
    unmeasured_path = ''
    if setup or not os.path.exists('locations.txt'):
        while True:
            click.echo(inst("Please provide the paths to each folder\nIf you need help type 'quit'; then run 'florets --help'",True))
            originals_path = input('Originals absolute Path: ')
            if originals_path == 'quit':
                exit()

            measured_path = input('Measured absolute Path: ')
            unmeasured_path = input('Unmeasured absolute Path: ')
            #processing the input
            ##removing \ symbols for mac/linux
            originals_path = originals_path.replace("\\ "," ")
            measured_path = measured_path.replace("\\ "," ")
            unmeasured_path = unmeasured_path.replace("\\ "," ")
            ## replacing \ with / symbol, windows
            originals_path = originals_path.replace("\\","/")
            measured_path = measured_path.replace("\\","/")
            unmeasured_path = unmeasured_path.replace("\\","/")
            ##removing " symbols
            originals_path = originals_path.replace("\"","")
            measured_path = measured_path.replace("\"","")
            unmeasured_path = unmeasured_path.replace("\"","")
            ##removing trailing space
            if originals_path.endswith(' '):
                originals_path = originals_path[:-1]
            if measured_path.endswith(' '):
                measured_path = measured_path[:-1]
            if unmeasured_path.endswith(' '):
                unmeasured_path = unmeasured_path[:-1]

            #checking for valid paths
            if os.path.exists(originals_path) and os.path.exists(measured_path) and os.path.exists(unmeasured_path):
                break
            else:
                originals_path = originals_path[1:-1]
                measured_path = measured_path[1:-1]
                unmeasured_path = unmeasured_path[1:-1]
                if os.path.exists(originals_path) and os.path.exists(measured_path) and os.path.exists(unmeasured_path):
                    break
                else:
                    click.echo(bad('*****One or more paths are invalid*****',True))
                    
        with open('locations.txt','w') as f:
            f.write(f"""#originals_path = '{originals_path}'\n#measured_path = '{measured_path}'\n#unmeasured_path = '{unmeasured_path}'""")
        
    else:
        ls = os.listdir()
        if 'locations.txt' in ls:
            with open('locations.txt','r') as loc:
                locations_text = loc.read()
            originals_path = re.findall("#originals_path = '(.+)'",locations_text)[0]
            measured_path = re.findall("#measured_path = '(.+)'",locations_text)[0]
            unmeasured_path = re.findall("#unmeasured_path = '(.+)'",locations_text)[0]
            if os.path.exists(originals_path) and os.path.exists(measured_path) and os.path.exists(unmeasured_path):
                click.echo(good("Paths confirmed",True))
            else:
                click.echo(bad('One or more paths in save file are invalid, please re-run with florets --setup',True))
        
    print(startup_message)
    print('Originals Path -> ',originals_path)
    print('Unmeasued Path -> ',unmeasured_path)
    print('Measured Path -> ', measured_path)
    while True:
        click.echo(question('Are the paths correct?',True))
        ok_to_continue = input('[y/n]: ')
        if (ok_to_continue == 'y' or ok_to_continue == 'n'):
            break
        
    if ok_to_continue == 'y':
        click.echo(good('Running...',True))
    else:
        click.echo(bad('\n**Try starting again with florets --setup\n\n',True))
        exit()
    # if not os.path.exists(measured_path+'/'+'master_result.csv'):
    #     with open(measured_path+'/'+'master_record.csv','w') as f:
    #         f.write('')
    if not os.path.exists(measured_path+'/'+'archived_results'):
        os.mkdir(measured_path+'/'+'archived_results')
    
    removed = [] #used to ensure it doesnt delete the newest .tiff file
    while True:
        originals = [re.findall(reg_format,fn) for fn in os.listdir(originals_path)]
        originals = [t for t in originals if len(t) > 0]
        measured = [re.findall(reg_format,fn) for fn in os.listdir(measured_path)]
        measured = [t for t in measured if len(t) > 0]
        unmeasured = [re.findall(reg_format,fn) for fn in os.listdir(unmeasured_path)]
        unmeasured = [t for t in unmeasured if len(t) > 0]
        assert len(unmeasured) > 0, 'Debug:: empty unmeasured list'
        for fname in originals:
            if fname[0][0] not in [un[0][0] for un in unmeasured] and fname[0][0] not in [m[0][0] for m in measured]:
                name = fname[0][0]
                ext = fname[0][1]
                source = originals_path + '/' + name + ext
                destination = unmeasured_path
                shutil.copy(source,destination)
                click.echo(f"added '{good(name + ext,True)}' to unmeasured -- {inst(datetime.now(),True)}")
        for fname in unmeasured:
            if fname[0][0] in [m[0][0] for m in measured]:
                name = fname[0][0]
                ext = fname[0][1]
                if [name,ext] not in removed:
                    removed.append([name,ext])
        for name,ext in removed:
            if name != removed[-1][0]:
                source = unmeasured_path + '/' + name + ext
                try:
                    os.remove(source)
                    click.echo(f"removed '{good(name + ext,True)}' from unmeasured -- {inst(datetime.now(),True)}")
                    removed.remove([name,ext])
                except:
                    print('Debug:: Please Restart Srcipt')
                    print(removed)
        
        
        for fname in measured:
            name = fname[0][0]
            ext = fname[0][1]
            if ext == '.csv' and name != 'master_result':
                source = measured_path+'/'+name+ext # name of the .csv file to move
                new_file_name = name+ext
                i = 1 # increment for file naming
                while os.path.exists(measured_path+'/archived_results/'+new_file_name): # increments the filename to make it unique
                    i += 1
                    new_file_name = name+str(i)+ext
                    if i >= 1000:
                        click.echo(bad("An error has occured while trying to rename the csv file"))
                    
                destination = measured_path+'/archived_results/'+new_file_name
                try:
                    shutil.move(source,destination)
                    click.echo(f"moved {good(name+ext,r=True)} to {inst('archived_results/',r=True)}")
                except:
                    click.echo(bad(f'An error occured while trying to move {name+ext}. Try incrementing the number at the end of the file name to make it unique.'))
                #combining result.csv's into a single master_result.csv
                csvs = {}
                for _file in os.listdir(measured_path+'/archived_results/'):
                    if _file.endswith(".csv"):
                        csvs.update({name+ext:pd.read_csv(measured_path+'/archived_results/'+_file)})
                master = pd.concat(list(csvs.values()))
                master = master[[" ","Label","Length"]]
                master.Length = master.Length.apply(lambda x: np.round(x/(2400/2.54),3) if x >=5 else x)
                master = master.rename(columns={' ':'original_index'})
                master.reset_index(inplace=True)
                master.to_csv(measured_path+'/master_result.csv',index=False)
                click.echo(f"{good(new_file_name+ext,r=True)} appended to {inst('master_record.csv',r=True)}")
                
        time.sleep(refresh)
        
    

if __name__ == '__main__':
    main()
    