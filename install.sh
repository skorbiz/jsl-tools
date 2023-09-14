#!/bin/bash
#set -x # Prints all line before execution
set -euo pipefail # Fail hard

# The user must not be root
# ============================
if [ "$(whoami)" == "root" ]; then
    echo "This script should not be run as root"
    exit 1
fi

# Find and goto this folder
# ============================
script_bash=${BASH_SOURCE[0]:-$0} 
jsl_tool_path=$(dirname "$(readlink -f "${script_bash}")") 
pushd "${jsl_tool_path}" >/dev/null || exit
echo " # Found jsl_tools at: ${jsl_tool_path}"
# BASH_SOURCE for when its defined, otherwise $0 (Which does not work with 'source' in all shells)


# Install pip dependencies
# ============================
if ! python3 -m pip --version >/dev/null 2>&1; then
    echo " # Please install python3 and pip.."
    exit 1
fi

if (pip -vvv freeze -r requirements.txt 2>&1 | grep "not installed") >/dev/null 2>&1; then
    echo " # Installing python dependencies for jsl_tool.."
    sudo python3 -m pip install --ignore-installed -r "requirements.txt"
fi

# Install to bashrc
# ============================

tag_begin="# JSL_TOOL_AUTOGEN_SOURCE_BEGIN ##"
tag_end="## JSL_TOOL_AUTOGEN_SOURCE_END ##"

# Delete the section if it exists
if grep -q "${tag_end}" ~/.bashrc
then
    echo " # Removing old jsl_tools from bashrc.."
    file_name=~/.bashrc
    current_time=$(date "+%Y.%m.%d-%H.%M.%S")
    new_fileName=$file_name."bak".$current_time
    cp "$file_name" "$new_fileName"
    sed -e "/^${tag_begin}/,/^${tag_end}/d" "$new_fileName" > "$file_name"
    rm "$new_fileName"
fi

# Re-add the section
echo " # Adding jsl_tools to bashrc.."
echo "
${tag_begin}
  if [ -f ${jsl_tool_path}/env.sh ]; then
    source ${jsl_tool_path}/env.sh
  else
    echo 'Failed to source ${jsl_tool_path}/env.sh'
  fi
${tag_end}
" >> ~/.bashrc


