# #!/usr/bin/env python3

# import json
import os
# import subprocess

import argparse

ROOT = os.path.expanduser("~/Dropbox/workspaces")

workspace_file = os.path.join(os.getcwd(), "JLA_WORKSPACE")
if os.path.exists(workspace_file):
    ROOT = os.path.dirname(workspace_file)
else:
    print("Did not find file {workspace_file}"
        "\n Defaulting to workspace: {root}".format(workspace_file=workspace_file, root=ROOT))


SHARED_DOCKER_RUN_ARGS = (
           #" --privileged"
		   # "--network=host",
            # "-v ${env:HOME}${env:USERPROFILE}/.ssh:/home/dev/.ssh-localhost:ro"
            # "-v ${env:SSH_AUTH_SOCK}:/ssh-agent"
            # "-e SSH_AUTH_SOCK=/ssh-agent"
            # "-u 637812433"
            # "--ipc=host"
            # "-v ${env:HOME}${env:USERPROFILE}/.docker:/home/dev/.docker"
            # "-v ${env:HOME}${env:USERPROFILE}/data:/data"
            # "-v /tmp/coredumps:/tmp/coredumps
            # // "-e",
            # // "NVIDIA_DRIVER_CAPABILITIES=all",
            # // "-e",
            # // "NVIDIA-VISIBLE_DEVICES=all",
            # // "-e",
            # // "QT_X11_NO_MITSHM=1"
            # // "--gpus", 
            # // "all", 
            # "-e", 
            # "NVIDIA_VISIBLE_DEVICES=all", 
            # "-e", 
            # "NVIDIA_DRIVER_CAPABILITIES=graphics"
            # // "-runtime", "nvidia"
           " -v /var/run/docker.sock:/var/run/docker.sock"
		   " -v /tmp/.X11-unix:/tmp/.X11-unix"
           " -e DISPLAY=unix{display}"
           # Nedded for RVIZ in ros noetic
           " --device /dev/dri:/dev/dri"
           ).format(display=os.environ['DISPLAY'])

def attach_to_developer_container(args):
    import os
    import subprocess

    find_container_cmd = 'docker container ls | grep "{}" | cut -d " " -f 1 | tr -d "\n" '.format("vsc-")
    container_name = subprocess.check_output(find_container_cmd, shell=True).decode('utf-8')

    os.execv("/usr/bin/docker", ["WIRED_PYTHON", "exec", "-it", container_name, "/bin/bash"])


def build_developer_container(args):
    import subprocess
    tag = "my_dev_container"
    dockerfile = os.path.join(ROOT, ".devcontainer/Dockerfile")
    cmd = "docker build -f {} -t {} {source_root}".format(dockerfile, tag, source_root=ROOT)
    print(cmd)
    subprocess.check_call(cmd.split())


def run_developer_container(args):
    import subprocess
    import pathlib
    args =(" --rm"
           " --name vsc-workspace-jla-tool-spawned"
           " --detach"
           " --tty"  # Allocating a tty connection prevents the container form exiting
           " -v {source_root}:/workspaces/{name}").format(source_root=ROOT, name=pathlib.PurePath(ROOT).name)
    args += SHARED_DOCKER_RUN_ARGS
    cmd = "docker run {args} my_dev_container".format(args=args)
    print(cmd)
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
    # os.rename(path, path_backup)
    return path_backup


def create_tar(output_filename, source_dir):

    def filter(tar_info):
        for e in [".git", "__pycache__", ".pyc"]:
            if e in tar_info.name:
                return None
        return tar_info

    import tarfile
    with tarfile.open(output_filename, "w:") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir), filter=filter)


def init_developer_environment(args):
    from jinja2 import Environment, FileSystemLoader
    path_out_dir = os.path.join(ROOT, ".devcontainer")
    path_template_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "template")

    path_backup_dir = ""
    if os.path.exists(path_out_dir):
        path_backup_dir=backup_dir(path_out_dir)

    from distutils.dir_util import copy_tree
    copy_tree(path_template_dir, path_out_dir)

    path_jla_tools_tar = os.path.join(path_out_dir, "assets", "jla_tools.tar")
    path_jla_tools = os.path.expanduser("~/Dropbox/workspaces/jla_tools")
    create_tar(path_jla_tools_tar, path_jla_tools)

    environment = Environment(loader=FileSystemLoader(path_out_dir))
    for filename in ["devcontainer.json", "Dockerfile"]:
        template_file = os.path.join(filename + ".jinja2")
        out_file = os.path.join(path_out_dir, filename)
                
        template = environment.get_template(template_file)
        content = template.render(
            base_image = args.base_image,
            install_ros1 = args.with_ros1,
            install_ros2 = not args.without_ros2,
            docker_run_args = SHARED_DOCKER_RUN_ARGS.split(),
            local_user_id = os.getuid(),
            local_group_id = os.getgid())
        
        with open(out_file, mode="w", encoding="utf-8") as out:
            out.write(content)
            print(f"... wrote {filename}")
        os.remove(os.path.join(path_out_dir, template_file))
    
    print_diff_warning_if_needed(path_out_dir, path_backup_dir)
    ## Todo Add user uid and gui to template files
        

def add_parsers(parser):
    dev_parser = parser.add_parser('devcontainer', help='tools related to working within the development container', formatter_class=argparse.RawTextHelpFormatter)
    dev_subparser = dev_parser.add_subparsers()

    init_parser = dev_subparser.add_parser("init", help="""Init setup files and configures the dev container with Jinja2.""")
    init_parser.add_argument("--base_image", default="ubuntu:22.04", choices=('ubuntu:22.04', 'ubuntu:20.04'), help="Specify base image")
    init_parser.add_argument("--with_ros1", action='store_true')
    init_parser.add_argument("--without_ros2", action='store_true')
    init_parser.set_defaults(func=init_developer_environment)

    build_parser = dev_subparser.add_parser("build", help="""Builds the dev container using Docker build -- as an alternative to building/running in vs-code""")
    build_parser.set_defaults(func=build_developer_container)

    run_parser = dev_subparser.add_parser("run", help="""Runs the dev container -- as an alternative to building/running in vs-code" """)
    run_parser.set_defaults(func=run_developer_container)

    run_parser = dev_subparser.add_parser("attach", help="""Attaches to the existing dev container.""")
    run_parser.set_defaults(func=attach_to_developer_container)

    

