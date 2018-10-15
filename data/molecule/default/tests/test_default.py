import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_sample(host):
    # ans_fact = host.ansible('setup')['ansible_facts']
    # ans_vars = host.ansible.get_variables()
    # var_file = ans_vars['playbook_dir'] + '/tests/__pycache__/' + ans_vars['inventory_hostname'] + '.yml'
    # host_vars = yaml.load(open(var_file, 'r'))

    f = host.file('/etc/hosts')
    assert f.exists
    assert f.is_file
    assert f.is_directory
    assert f.is_symlink
    assert f.linked_to == '/run/lock'
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == '0600'
    assert f.contains('test string')

    assert host.package('package_name').is_installed
    for pkg in role_packages:
        assert host.package(pkg).is_installed
