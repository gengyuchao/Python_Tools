# Python_Tools
Python Tools create by myself.

```
c_func_tools.py 
    -r <read file> 
    -l <count lines> 
    -f <count function num> 
    -t <get func type> 
    -s <save known func type to ./type_list.txt> 
    -c <create fake func> 
    -a <Directory recursive execution> 
    --clean <Clean temp file>
    
```
- Example

```
python3 c_func_tools.py -t c_file -c c_file
python3 c_func_tools.py -a -t project_dir -s -a -c project_dir
```
The Refactor function will save in the `temp` file.


origin File
```
#include "stdio.h"

const void* test_func( void* test2)
{
    void *p = NULL;
    return p;
}
```
Auto Refactor file
```
#include "stdio.h"

#include "fake_test_header.h" 
void gyc_dbg_trace_start(const void * func_addr,char* data); 
void gyc_dbg_trace_end(const void * func_addr,char* data);

const void* test_func( void* test2)
{
	void * return_value;
	gyc_dbg_trace_start((void *)test_func,NULL);
	return_value = 	test_func_fake(   test2 ) ;
	gyc_dbg_trace_end((void *)test_func,NULL);
	return return_value; 
}

void * test_func_fake( void * test2 ) 
{
    void *p = NULL;
    return p;
}

```


Analisys Tools 

```
-R < Record_Time >
-D < Start Do it>
-G < Get Func addr and Create a function dictionary >
-F < Formate The log File according the function dictionary >

```

```
python3 gyc.py -RG ./you_log_File.txt -D -RF ./you_log_File.txt -D
```