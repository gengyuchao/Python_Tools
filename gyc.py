import sys
import getopt
import time
import re
import os
import readline
import shutil
import datetime

def test_func(param):
    print ("test_func")

def Record_program_running_time(execute_func,param):
    func_start_time = datetime.datetime.now()
    execute_func(param)
    func_end_time = datetime.datetime.now()
    localtime = time.asctime( time.localtime(time.time()) )
    print("\n=====================================" + localtime + "\n用时: %s s\n" %(func_end_time - func_start_time))

Func_Table = {0:"name"}
def get_func_address(read_file_name):
    Func_name = 1
    Func_addr = 2
    Can_Auto_Analisys = False
    try:
        fhand = open (read_file_name)
    except:
        print ('打开文件出错:', read_file_name)
        exit ()
    for line in fhand:
        
        if Can_Auto_Analisys == False:
            if line.find("#Functions_Table Start#")!=-1:
                Can_Auto_Analisys = True
            # else :
            #     print(line)
            continue

        if Can_Auto_Analisys == True:
            if line.find("#Functions_Table End#")!=-1:
                Can_Auto_Analisys = False
                continue

        orig_line = line
        split_str = '[ :,\n\t]'
        words = re.split(split_str,line)
        while ' ' in words:
            words.remove(' ')
        while '' in words:
            words.remove('')
        while ',' in words:
            words.remove(',')
        while ',' in words:
            words.remove('\t')
        print(words)
        
        Func_Table[words[Func_addr].replace("0x","")]=words[Func_name]
        # Show_list_str = ""
        # Show_list_str = Show_list_str + words[Run_Time] + "\t"
        # for i in range(0,int(words[Deep])):
        #     Show_list_str = Show_list_str+"| "
        # Show_list_str = Show_list_str+"|-"
        # Show_list_str = Show_list_str + words[Func_addr]
    print(Func_Table)

def Format_dbg_info_2_str(read_file_name):
    Deep = 0
    Func_addr = 1
    Run_Time = 2
    try:
        fhand = open (read_file_name)
    except:
        print ('打开文件出错:', read_file_name)
        exit ()
    for line in fhand:
        orig_line = line
        if line.find('|')==-1:
            print(orig_line)
            continue
        words = line.split('|')
        while ' ' in words:
            words.remove(' ')
        while '' in words:
            words.remove('')
        # print(words)
        Show_list_str = ""
        Show_list_str = Show_list_str + words[Run_Time] + "\t"
        for i in range(0,int(words[Deep])):
            Show_list_str = Show_list_str+"| "
        Show_list_str = Show_list_str+"|-"
        if words[Func_addr] in Func_Table.keys() :
            Show_list_str = Show_list_str + Func_Table[words[Func_addr]]
        else :
            Show_list_str = Show_list_str + words[Func_addr]
        
        print(Show_list_str)


        # //print(orig_line)

# // //         ptr_log[log_count++] = '|';
# // //         for(int i = 0 ; i < deep_of_func -1 ;i++) {
# // //             ptr_log[log_count++] = '|';
# // //             ptr_log[log_count++] = ' ';
# // //         }
# // //         ptr_log[log_count++] = '|';
# // //         ptr_log[log_count++] = '-';

Help_menu = "\
gyc.py \
-h < Show this help menu > \
-R < Record_Time > \
-D < Start Do it> \
-G < Get Func addr and Create a function dictionary > \
-F < Formate The log File according the function dictionary > \
"


def main(argv):

    try:
        opts, args = getopt.getopt(argv, "hRDF:G:c:a", ["countlines=","rfile=","clean"])
    except getopt.GetoptError:
        print ('error-' + Help_text)
        return
    
    Flag_Record_Time = False
    Func_arg = None
    Flag_Do_it = False
    for opt, arg in opts:
        if opt == '-h':
            print (Help_menu)
            sys.exit()
        elif opt in ("-R", "--Record_Time"):
            Flag_Record_Time = True
        elif opt in ("-D", "--do_it"):
            Flag_Do_it = True
        elif opt in ("-F", "--Formate"):
            execute_func = Format_dbg_info_2_str
            Func_arg = arg
        elif opt in ("-G", "--Get_Func_addr"):
            execute_func = get_func_address
            Func_arg = arg


        if Flag_Do_it == True:
            Flag_Do_it = False
            if Flag_Record_Time == True:
                Record_program_running_time(execute_func,Func_arg)
            else :
                file_name = arg
                if os.path.isdir(arg):
                    print(arg+" is not a file.")
                else :
                    execute_func(file_name)


        
if __name__ == "__main__":
    main(sys.argv[1:])
