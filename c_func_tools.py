
import sys
import getopt

import time
import re
import os
import readline
import shutil

def function_read_file(file_name):
    "读文件，并打印"
    print("Read File:")
    print(file_name)

    try:
        file = open(file_name, 'r')
        print(file.read())
    finally:
        if file:
            file.close()
    return

def function_count_file_line( parameters ):
    "读文件，并统计行数"
    filename = parameters
    count = 0 
    with open(filename) as fhand:
        for line in fhand:
            count = count + 1
        print ('总共的行数: %d' % (count))
    return count


C_descriptor_list = ['const','volatile','extern','static', 'register','auto','*']
C_special_descriptor_list = ['const','IRAM_ATTR','DRAM_ATTR','*']

C_type_list =["unsigned int","unsigned char",
"uint64_t","uint32_t","uint16_t","uint8_t",
"int64_t","int32_t","int16_t","int8_t","u8","u16","u32",
"void","int","bool","char","float","short","long","double"
]

split_str = '([ ()\n\s,=;*])'

def is_Bracket_matching(s):
    l = ['{','}','[',']','(',')']
    res = []
    for i in s:
        if i in l:
            res.append(i)
    resStr  = ''.join(res)
    while '()' in resStr or '{}' in resStr or '[]' in resStr:
        resStr = resStr.replace('()','').replace('{}','').replace('[]','')
    if resStr == '':
        return True
    return False


MAX_func_name_len = 600

def function_count_all_function(filename):
    func_count_number = 0
    try:
        fhand = open (filename)
    except:
        print ('打开文件出错:', filename)
        exit ()
    # 保存之前至少 3 个元素，防止因换行漏判
    last_3_word = ['first','second','thrid']
    for line in fhand:
        line = line.rstrip()
        words = last_3_word + re.split(split_str,line)           # 分割单词，以列表返回
        last_3_word = words[-3:]
        func_define = ""
        while ' ' in words:
            words.remove(' ')
        while '' in words:
            words.remove('')

        for i in range(0,len(words)-2):

            if i>0 and words[i-1] in C_descriptor_list :
                func_define = words[i-1] +" "
            else :
                func_define = ""
                # print(line)
                # print("is 0" + words[i-1] + "1" + words[i] + "2" + words[i+1] + "3" + words[i+2])

            if words[i] in C_type_list :
                temp_next_brackets = 2
                for word in words[ i:i + 3 ] :
                    if word in C_special_descriptor_list:
                        temp_next_brackets = temp_next_brackets + 1
                        # print (words)
                        # print (temp_next_brackets)
                if i + temp_next_brackets >= len(words):
                    continue
                func_name = words[ i + temp_next_brackets - 1 ]
                if func_name.find("[")!=-1 or func_name.find("(")!=-1 or func_name.find(")")!=-1 or func_name.find("=")!=-1:
                    # print("Find error name"+ func_name)
                    # print(words)
                    break
                if words[ i + temp_next_brackets ] =='(':
                    define_count = 0
                    while words[i]!='{' and define_count < MAX_func_name_len:
                        define_count = define_count + 1
                        if words[i] == ';'or words[i] == '}':
                            break

                        if words[i] != '\n' and  words[i] != ' ' :
                            # print("["+words[i])
                            func_define += words[i] + ' '  
                        i=i+1                        
                        if i >= len(words):
                            line = fhand.readline()
                            line = line.rstrip()
                            line = re.split(split_str,line)
                            words =  line
                            i = 0
                            # print(words)
                    if words[i]=='{':
                        print(func_define)
                        func_count_number = func_count_number + 1
                    break

    fhand.close()
    print("\n"+filename+" have "+str(func_count_number) +" functions.")
    return func_count_number


type_list_save = C_type_list

def function_search_all_type(filename):
    if filename.find(".c")==-1 and filename.find(".h")==-1 :
        print(filename+" is not target file.")
        return
    try:
        fhand = open (filename)
    except:
        print ('打开文件出错:', filename)
        exit ()
    
    for line in fhand:
        line = line.rstrip()
        words = re.split(split_str,line)           # 分割单词，以列表返回
       
        while ' ' in words:
            words.remove(' ')
        while '' in words:
            words.remove('')

        for i in range(0,len(words)-2):
            if words[i].endswith("_t")==True or words[i].endswith("_t*")==True :
                if words[i] not in type_list_save:
                    while words[i].find('"') != -1:
                        words[i] = words[i].replace('"',"")
                    while words[i].find('/') != -1:
                        words[i] = words[i].replace('/',"")
                    print('"'+ words[i] +'",')
                    type_list_save.insert(0,words[i])
            

    fhand.close()# 


def function_package_debug_functions(func_type,func_special_des,func_name,func_param):
    param_in = func_param
    for C_type in C_type_list:
        if(param_in.find(C_type)!=-1):
            param_in = param_in.replace(C_type,"")
    for C_descriptor in C_descriptor_list:
        if(param_in.find(C_descriptor)!=-1):
            param_in = param_in.replace(C_descriptor,"")


    if(param_in.find("struct")!=-1):
        param_in = re.split(split_str,param_in)
        print(param_in)
        while ' ' in param_in:
            param_in.remove(' ')
        while '' in param_in:
            param_in.remove('')
        while 'struct' in param_in:
            param_in.remove(param_in[param_in.index('struct')+1])
            param_in.remove(param_in[param_in.index('struct')])
            print(param_in)
        
        param_in = " ".join(param_in)
        # print(param_in.find("struct"))
        # print(param_in.find(" ",param_in.find("struct")))
        # print(param_in[:param_in.find(" ",param_in.find("struct")-1)] + param_in[param_in.find(" ",param_in.find("struct")+7):] )
        # param_in = param_in.replace("struct","")

    func_str="{\n\t"

    Flag_is_void_type = (func_type=="void") 
    Flag_is_point_type = "*" in func_special_des
    
    if Flag_is_point_type == True :
        Flag_is_void_type = False

    if Flag_is_point_type == True:
        func_str = func_str + func_type + " *" + " return_value;\n\t"
    elif Flag_is_void_type == False:
        func_str = func_str + func_type + " return_value;\n\t"
    
    func_str = func_str + "gyc_dbg_trace_start((void *)"+func_name+",NULL);\n"

    if Flag_is_void_type == False:
        func_str = func_str + "\treturn_value = "
    func_str = func_str + "\t"+func_name+"_fake"+param_in+";\n"+\
    "\tgyc_dbg_trace_end((void *)"+func_name+",NULL);\n"
    if Flag_is_void_type == False:
        func_str = func_str + "\treturn return_value; \n"
    func_str = func_str + "}\n\n"+\
    func_type+ " " +" ".join(func_special_des) + " "+func_name+"_fake"+func_param+\
    "\n{\n"

    print("param:" + func_param)
    return func_str

def function_Refactor_all_functions(filename):
    "重构所有函数"

    try:
        fhand = open (filename)
    except:
        print ('打开文件出错:', filename)
        exit ()
    
    (file_dir, file_name) = os.path.split(fhand.name)
    print (file_dir)
    print (file_name)

    new_file_dir = './temp/'+file_dir+'/'
    if not os.path.exists(new_file_dir):
        os.makedirs(new_file_dir)
    new_file_location = new_file_dir + file_name

    if file_name.find(".c")==-1 :
        print(file_name+" is not a .c file")
        # adding exception handling
        try:
            shutil.copy(filename, new_file_location)
        except IOError as e:
            print("Unable to copy file. %s" % e)
        except:
            print("Unexpected error:", sys.exc_info())

        return
    
    write_file = open(new_file_location, 'w')
    write_file_header = open(new_file_dir+'fake_'+file_name[0:-2]+'_header.h', 'w')
    write_file_header.write("#ifndef __"+file_name[0:-2].upper()+"_H__\n#define __"+file_name[0:-2].upper()+"_H__\n\n")

    # 保存之前至少 3 个元素，防止因换行漏判
    has_add_debug_info = False
    last_3_word = ['ab','bb','cb']

    Temp_head_list = C_descriptor_list + C_type_list +["#define"]
    Temp_head_list.remove("*")
    for line in fhand:
        orig_line = line
        line = line.rstrip()
        words = last_3_word + re.split(split_str,line)           # 分割单词，以列表返回
        last_3_word = words[-3:]
        func_define = ""

        # 去除掉无用的 空格 和 空的元素，防止干扰
        while ' ' in words:
            words.remove(' ')
        while '' in words:
            words.remove('')
        
        for i in range(0,len(words)-2):

            if has_add_debug_info == False and (words[i] in Temp_head_list):
                has_add_debug_info = True
                write_file.write('#include '+'"fake_'+file_name[0:-2]+'_header.h"'+' \nvoid gyc_dbg_trace_start(const void * func_addr,char* data); \nvoid gyc_dbg_trace_end(const void * func_addr,char* data);\n\n')

            if i>0 and (words[i-1] in C_descriptor_list) :
                func_define = words[i-1] +" "
            else :
                func_define = ""

            if words[i] in C_type_list :
                temp_next_brackets = 2
                func_type = words[i]
                func_param = ""
                func_special_des = []
                for word in words[ i:i + 3 ] :
                    if word in C_special_descriptor_list:
                        # print(words[ i:i + 3 ])
                        # print(word)
                        func_special_des.append(word)
                        temp_next_brackets = temp_next_brackets + 1
                # 如果读取的文件不完整（有其他内容在下一行），则下次再处理
                if i + temp_next_brackets >= len(words):
                    continue
                func_name = words[ i + temp_next_brackets -1]
                if func_name.find("[")!=-1 or func_name.find("(")!=-1 or func_name.find(")")!=-1:
                    # print("Find error name"+ func_name)
                    # print(words)
                    break
                if words[ i + temp_next_brackets ] =='(':
                    # i = i + temp_next_brackets
                    while words[i]!='{' :
                        find_func_param_finish = (func_param != "" and is_Bracket_matching(func_param) == True)
                        # 如果函数参数已经获取完成，但是下一个元素不是{ 而且不是注释
                        if find_func_param_finish == True:
                            print("finish:"+func_param)
                        if find_func_param_finish == True :
                            if words[i].find('//')!=-1: #如果这是注释
                                while i<len(words)-2: # 如果没有遇到*/
                                    i = i+1
                                continue
                            if words[i].find('/')!=-1 and words[i+1].find('*')!=-1: #如果这是注释
                                print("find /*")
                                i=i+2
                                while i<len(words) : # 如果没有遇到*/
                                    print("#"+ words[i])
                                    i = i+1
                                    if words[i].find('*')==-1:
                                        break
                            else :
                                print(words[i:])
                                print ("Error : 可能是注释，跳过")
                                break
                        # 如果找到第一个 ‘(’ 将其写入 func_param, 如果写入过 '(' 则判断括号匹配
                        if words[i].find("(") != -1 or func_param != ""and is_Bracket_matching(func_param)==False:
                            func_param = func_param + words[i] + " "
                            # print(words[i])
                            # print(func_param)

                        if words[i] == ';' or words[i] == '}':
                            break
                        if words[i] != '\n' and  words[i] != ' ' :
                            # print("["+words[i])
                            func_define += words[i] + ' '  
                        i=i+1                        
                        if i >= len(words):
                            line = fhand.readline()
                            if orig_line != "":
                                write_file.write(orig_line)
                                orig_line = ""
                            if line.find("{")==-1:
                                write_file.write(line)
                            else : #如果存在{
                                orig_line = line
                            line = line.rstrip()
                            line = re.split(split_str,line)
                            words = line
                            while ' ' in words:
                                words.remove(' ')
                            while '' in words:
                                words.remove('')
                            i = 0
                            # print(words)
                    # while end
                    if words[i] == '{':
                        write_file.write(orig_line.replace("{",function_package_debug_functions(func_type,func_special_des,func_name,func_param)))
                        orig_line = ""

                        print(func_define)
                        # print("name:"+func_name)
                        write_file_header.write(func_type+" "+func_name+"_fake"+" "+func_param+";\n")
                    
                    # write_file.write('\n'+func_define+'\n')
                    break
                
        if orig_line != "" :
            write_file.write(orig_line)


    write_file_header.write("\n\n#endif\n")    

    fhand.close()# 
    write_file.close()
    write_file_header.close()

Help_text ="c_func_tools.py \n\
    -r <read file> \n\
    -l <count lines> \n\
    -f <count function num> \n\
    -t <get func type> \n\
    -s <save known func type to ./type_list.txt> \n\
    -c <create fake func> \n\
    -a <Directory recursive execution> \n\
    --clean <Clean temp file> \n\
"

def function_execute_for_all_file_in_dir(exe_function,exe_dir):

    localtime = time.asctime( time.localtime(time.time()) )
    print ("启动时间为 :", localtime)

    g = os.walk(exe_dir)  
    for path,dir_list,file_list in g:  
        for file_name in file_list:  
            print(file_name)
            (file_dir, file_type) = os.path.splitext(file_name)
            exe_function(os.path.join(path, file_name))

    localtime = time.asctime( time.localtime(time.time()) )
    print ("结束时间为 :", localtime)


def function_save_type_in_file(file_name):
    try:
        type_list_file = open('./type_list.txt', 'w')
    except:
        print ('打开文件出错:', filename)
        exit ()
    
    type_list_str = '"'+'","'.join(type_list_save)+'"'
    type_list_file.write(type_list_str)

def function_clean_file(file_name):
    # 清理缓存文件
    try :
        os.remove('./type_list.txt') 
        print ("Clean type_list.")
    except:
        if os.path.exists('./type_list.txt'):
            print ("clean type_list.txt fail.")

    try :
        #递归的删除目录及文件
        shutil.rmtree('./temp') 
        print ("Clean temp.")
    except:
        if os.path.exists('./temp'):
            print ("clean temp file fail.")
    
    print ("Clean success.")

def main(argv):
    read_file = ''
    outputfile = ''
    
    try:
        opts, args = getopt.getopt(argv, "hsr:f:l:t:c:a", ["countlines=","rfile=","clean"])
    except getopt.GetoptError:
        print ('error-' + Help_text)
        return
    
    dir_exe_func = False
    execute_func = None
    for opt, arg in opts:
        if opt == '-h':
            print (Help_text)
            sys.exit()
        elif opt in ("-r", "--rfile"):
            execute_func = function_read_file
        elif opt in ("-l", "--countlines"):
            execute_func = function_count_file_line
        elif opt in ("-f", "--funcname"):
            execute_func = function_count_all_function
        elif opt in ("-t", "--type_get"):
            execute_func = function_search_all_type
        elif opt in ("-c", "--create_file"):
            execute_func = function_Refactor_all_functions
        elif opt in ("-a", "--all_execu"):
            dir_exe_func = True        
        elif opt in ("-s", "--save_type_list"):
            execute_func = function_save_type_in_file
        elif opt in ("--clean"):
            execute_func = function_clean_file

        if opt not in ("-a", "--all_execu") and execute_func != None:
            if dir_exe_func == True:
                dir_exe_func = False
                read_dir = arg
                if os.path.isfile(arg):
                    print(arg+" is not a path.")
                else :
                    function_execute_for_all_file_in_dir(execute_func,read_dir)
            else :
                file_name = arg
                if os.path.isdir(arg):
                    print(arg+" is not a file.")
                else :
                    execute_func(file_name)


        
if __name__ == "__main__":
    main(sys.argv[1:])
