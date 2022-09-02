## How I installed the mingw ?

##### Just run the mingw installer with GUI selected and select base utils with G++ option selected 

## How i added the env variable

### dont rerun --> messes up the env tree 

code~
```c
$new_entry = 'c:\a\bin;c:\b\cmd;c:\c\bin'

$old_path = [Environment]::GetEnvironmentVariable('path', 'user');
$new_path = $old_path + ';' + $new_entry
[Environment]::SetEnvironmentVariable('path', $new_path,'user');
```
~

### if i want to search before doing anything 

```c
$new_entry = 'c:\blah'
$search_pattern = ';' + $new_entry.Replace("\","\\")

$old_path = [Environment]::GetEnvironmentVariable('path', 'user');
$replace_string = ''
$without_entry_path = $old_path -replace $search_pattern, $replace_string
$new_path = $without_entry_path + ';' + $new_entry
[Environment]::SetEnvironmentVariable('path', $new_path,'user');
```

[set compiler at cmake](https://stackoverflow.com/questions/11269833/cmake-selecting-a-generator-within-cmakelists-txt)


or 

### win + R
--> rundll32 sysdm.cpl, EditEnvironmentVariables

### python packages i need
- openpyxl
- pandas
- tensorflow
- scipy (included)
- numpy (included)
- meson

### software we need
- bring git online
  - for git set env at cmd dir
- GCC and g++ compiler for c++
  - for GCC compiler set env at /bin dir
- cmake to be configured correctly if(meson soooo good leave cmake xD)
- once python is up and running --> meson and ninja to be installed
- once python and all others completed we need JULIA
- sqlite for database related topics

### apart from those
- keepassXc
- chrome / brave
- obsidian
- VS code


### cmake hacks to set compiler ---> run 2 times to build properly

```c

cmake_minimum_required(VERSION 3.2)
set(CMAKE_GENERATOR "MinGW Makefiles" CACHE INTERNAL "" FORCE)

# change the path to compiler here
set(CMAKE_C_COMPILER_FORCED "C://a//bin//gcc.exe")
set(CMAKE_CXX_COMPILER_FORCED "C://a//bin//g++.exe")

#set(CMAKE_C_COMPILER "D://C_Compilers//mingw64//bin//gcc.exe")
#set(CMAKE_CXX_COMPILER "D://C_Compilers//mingw64//bin//g++.exe")

project(prmix VERSION 0.1)
#add_executable(output test.cpp)
add_executable(output PR_mix.h PR_mix.cpp approach2.cpp)

```

In some endpoints --> cisco repeated read and write raises as ransomeware
so julia precompilation does not work.