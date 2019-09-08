import os
import yaml
import glob
# import pytest
# import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

role_vars = role_default_vars = {}
role_default_var_file = os.environ['MOLECULE_PROJECT_DIRECTORY'] + '/defaults/main.yml'
if os.path.exists(role_default_var_file):
    role_default_vars.update(yaml.full_load(open(role_default_var_file, 'r')))
    role_vars.update(role_default_vars)

role_var_file = os.environ['MOLECULE_PROJECT_DIRECTORY'] + '/vars/main.yml'
if os.path.exists(role_var_file):
    role_vars.update(yaml.full_load(open(role_var_file, 'r')))

ansible_host_vars = {}
host_dump_var_dir = os.environ['MOLECULE_SCENARIO_DIRECTORY'] + '/dump_vars'
if os.path.exists(host_dump_var_dir):
    dump_var_files = glob.glob(host_dump_var_dir + '/*.yml')
    for dump_var_file in dump_var_files:
        inventory_hostname = os.path.basename(dump_var_file)[:-4]
        ansible_host_vars[inventory_hostname] = yaml.full_load(open(dump_var_file, 'r'))


# @pytest.mark.parametrize('name', ['packages1', 'packages2'])
# def test_package(host, name):
#     assert host.package(pkg).is_installed
#
# def test_config(host):
#     f = host.file('/etc/hosts')
#     assert f.exists
#     assert f.is_file
#     assert f.is_directory
#     assert f.is_symlink
#     assert f.linked_to == '/run/lock'
#     assert f.user == 'root'
#     assert f.group == 'root'
#     assert f.mode == 0o600
#     assert f.contains('test string')
#     host_vars = role_vars
#     inventory_hostname = host.ansible.get_variables()['inventory_hostname']
#     if inventory_hostname in ansible_host_vars.keys():
#         host_vars = ansible_host_vars[inventory_hostname]
