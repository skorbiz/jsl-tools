#!/bin/bash
# set -x # Prints all line before execution
# set -euo pipefail # Fail hard

# BASH_SOURCE for when its defined, otherwise $0 (Which does not work with 'source' in all shells)
script_bash=${BASH_SOURCE[0]:-$0} 
jsl_tool_path=$(dirname "$(readlink -f "${script_bash}")") 

if [[ ":$PATH:" != *":$jsl_tool_path:"* ]]; then
    PATH="${jsl_tool_path}:${PATH}"
fi

if [ -x "$(command -v register-python-argcomplete)" ]; then
   # only add to path if not already there
   eval "$(register-python-argcomplete jsl)"
fi