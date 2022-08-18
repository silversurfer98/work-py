How I installed the mingw ?

Just run the mingw installer with GUI selected and select base utils with G++ option selected 

# How i added the env variable

# dont rerun --> messes up the env tree 

code~
$new_entry = 'c:\a\bin;c:\b\cmd;c:\c\bin'

$old_path = [Environment]::GetEnvironmentVariable('path', 'user');
$new_path = $old_path + ';' + $new_entry
[Environment]::SetEnvironmentVariable('path', $new_path,'user');
~

# if i want to search before doing anything 
$new_entry = 'c:\blah'
$search_pattern = ';' + $new_entry.Replace("\","\\")

$old_path = [Environment]::GetEnvironmentVariable('path', 'user');
$replace_string = ''
$without_entry_path = $old_path -replace $search_pattern, $replace_string
$new_path = $without_entry_path + ';' + $new_entry
[Environment]::SetEnvironmentVariable('path', $new_path,'user');


https://stackoverflow.com/questions/11269833/cmake-selecting-a-generator-within-cmakelists-txt


or 

## win + R
--> rundll32 sysdm.cpl, EditEnvironmentVariables