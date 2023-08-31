# #!/usr/bin/env python3

# import json
import os
# import subprocess

import argparse

ROOT = os.path.expanduser("~/Dropbox/workspaces")

SHARED_DOCKER_RUN_ARGS = (
           #" --privileged"
           " -v /var/run/docker.sock:/var/run/docker.sock")

def attach_to_developer_container():
    import os
    import subprocess

    find_container_cmd = 'docker container ls | grep "{}" | cut -d " " -f 1 | tr -d "\n" '.format("vsc-workspace")
    container_name = subprocess.check_output(find_container_cmd, shell=True).decode('utf-8')

    os.execv("/usr/bin/docker", ["WIRED_PYTHON", "exec", "-it", container_name, "/bin/bash"])


def build_developer_container():
    import subprocess
    tag = "my_dev_container"
    dockerfile = os.path.join(ROOT, ".devcontainer/Dockerfile")
    subprocess.check_call("docker build -f {} -t {} {source_root}".format(dockerfile, tag, source_root=ROOT).split())



def run_developer_container(cmd_in=None):
    import subprocess
    args =(" --rm"
           " --name vsc-workspace-jla-tool-spawned"
           " --detach"
           " --tty"  # Allocating a tty connection prevents the container form exiting
           " -v {source_root}:/workspaces/workspaces").format(source_root=ROOT)
    args += SHARED_DOCKER_RUN_ARGS

    cmd = "docker run {args} my_dev_container".format(args=args)
    # cmd = cmd.format(uid=os.getuid())
    if cmd_in:
        cmd += " /bin/bash -c {}".format(cmd_in)

    subprocess.check_call(cmd.split())



def print_diff_warning_if_needed(dir1, dir2):
    import difflib
    for file in os.listdir(dir1):      
        try:
            with open(os.path.join(dir1, file), mode="r") as f1, open(os.path.join(dir2, file), mode="r") as f2:
                # diff = difflib.ndiff(f1.readlines(), f2.readlines()) # Full file diff
                diff = ''.join(difflib.unified_diff(f1.readlines(), f2.readlines()))
                if diff:
                    print("Warning: diff detected in {}... could be the dec container template changed or you made local changes".format(file))
                    print(diff, end="")
        except (FileNotFoundError, IsADirectoryError, UnicodeDecodeError):
            pass
        except Exception as e:
            print("An exception of type {} occurred. Arguments:{}".format(type(e).__name__, e.args))
            print(e)

def backup_dir(path):
    import datetime
    from distutils.dir_util import copy_tree
    time_string = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")   
    path_backup = path+"-backup-{}".format(time_string)
    # copy_tree(path, path_backup)
    return path_backup


def init_developer_environment():
    from jinja2 import Environment, FileSystemLoader
    path_out_dir = os.path.join(ROOT, ".devcontainer")
    path_template_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "template")

    path_backup_dir = ""
    if os.path.exists(path_out_dir):
        path_backup_dir=backup_dir(path_out_dir)

    from distutils.dir_util import copy_tree
    copy_tree(path_template_dir, path_out_dir)


    environment = Environment(loader=FileSystemLoader(path_out_dir))
    for filename in ["devcontainer.json", "Dockerfile"]:
        template_file = os.path.join(filename + ".jinja2")
        out_file = os.path.join(path_out_dir, filename)
                
        template = environment.get_template(template_file)
        content = template.render(docker_run_args=SHARED_DOCKER_RUN_ARGS.split())
        # args = '"'+'",\n"'.join(args)+'"'
        
        with open(out_file, mode="w", encoding="utf-8") as out:
            out.write(content)
            print(f"... wrote {filename}")
        os.remove(os.path.join(path_out_dir, template_file))
    
    print_diff_warning_if_needed(path_out_dir, path_backup_dir)
    ## Todo Add user uid and gui to template files
        

def developer_container(args):
    if args.init:
        return init_developer_environment()
    if args.build:
        return build_developer_container()
    if args.run:
        return run_developer_container()
    return attach_to_developer_container()


def add_parsers(parser):
    dev_parser = parser.add_parser('dev', help='tools related to working within the development container', formatter_class=argparse.RawTextHelpFormatter)
    dev_parser = dev_parser.add_subparsers()
    
    sub_parser = dev_parser.add_parser("container", help="""Attaches to the existing dev container.""")
    sub_parser.add_argument('--init', action='store_true')
    sub_parser.add_argument('--build', action='store_true')
    sub_parser.add_argument('--run', action='store_true')
    sub_parser.add_argument('--attach', action='store_true')
    sub_parser.set_defaults(func=developer_container)


