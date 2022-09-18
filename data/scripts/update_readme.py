#!/usr/bin/env python
import os
import re
import yaml

DS = os.sep
ROLE_ROOT = os.path.dirname(os.path.dirname(__file__))

if os.path.exists(ROLE_ROOT + DS + 'README.md'):
    role_name = os.path.basename(ROLE_ROOT)
    readme_description = ''
    readme_platform_text = ''
    readme_variables_text = ''
    readme_dependencies_text = ''
    readme_license_text = ''
    if os.path.exists(ROLE_ROOT + DS + 'meta' + DS + 'main.yml'):
        role_meta = yaml.safe_load(
            open(ROLE_ROOT + DS + 'meta' + DS + 'main.yml', 'r'))
        meta_keys = role_meta.keys()
        if 'galaxy_info' in meta_keys:
            galaxy_info_keys = role_meta['galaxy_info'].keys()
            if 'role_name' in galaxy_info_keys:
                role_name = role_meta['galaxy_info']['role_name']
            if 'description' in galaxy_info_keys:
                readme_description = role_meta['galaxy_info']['description']
            if 'license' in galaxy_info_keys:
                readme_license_text = role_meta['galaxy_info']['license']
            if 'platforms' in galaxy_info_keys:
                for platform in  role_meta['galaxy_info']['platforms']:
                    readme_platform_text += '### ' + platform['name'] + "\n"
                    readme_platform_text += "\n"
                    if 'versions' in platform.keys() and 'all' not in platform['versions']:
                        for platform_version in platform['versions']:
                            readme_platform_text += '- ' + platform_version + "\n"

        if 'dependencies' in role_meta.keys():
            for dependency in role_meta['dependencies']:
                if dependency is str:
                    readme_dependencies_text += '- ' + dependency + "\n"
                else:
                    dependency_keys = dependency.keys()
                    if 'role' in dependency_keys:
                        readme_dependencies_text += '- ' + dependency['role'] + "\n"
                    elif 'name' in dependency_keys:
                        readme_dependencies_text += '- ' + dependency['name'] + "\n"
                    elif 'src' in dependency_keys:
                        readme_dependencies_text += '- ' + dependency['src'] + "\n"

    if os.path.exists(ROLE_ROOT + DS + 'defaults' + DS + 'main.yml'):
        with open(ROLE_ROOT + DS + 'defaults' + DS + 'main.yml') as fp:
            var_docs = {}
            var_name = ''
            doc_block_lines = []
            for line in fp.readlines():
                if len(line.strip()) > 0:
                    match = re.search(r'^([a-zA-Z0-9_]+)\s?:\s+', line)
                    if match:
                        var_name = match.group(1)
                    else:
                        match = re.search(r'^#\s+(.+)', line)
                        if match:
                            doc_block_line = match.group(1)
                            if not re.search('^-+$', doc_block_line):
                                doc_block_lines.append(doc_block_line)
                else:
                    doc_block_lines = []
                    var_name = ''

                if len(var_name) > 0:
                    var_docs[var_name] = "\n".join(doc_block_lines)
                    doc_block_lines = []
                    var_name = ''

            if len(var_docs) > 0:
                for var_name, var_doc in var_docs.items():
                    readme_variables_text += '### `' + var_name + "`\n"
                    readme_variables_text += "\n"
                    if len(var_doc) > 0:
                        readme_variables_text += var_doc + "\n"
                        readme_variables_text += "\n"

    # Readmeのテキストを生成
    readme_text = role_name + "\n"
    readme_text += "=================\n"
    readme_text += "\n"
    if len(readme_description) > 0:
        readme_text += readme_description + "\n"
        readme_text += "\n"

    readme_platform_text = readme_platform_text.strip()
    if len(readme_platform_text) > 0:
        readme_text += "OS Platform\n"
        readme_text += "-----------------\n"
        readme_text += "\n"
        readme_text += readme_platform_text + "\n"
        readme_text += "\n"

    readme_variables_text = readme_variables_text.strip()
    if len(readme_variables_text) > 0:
        readme_text += "Role Variables\n"
        readme_text += "--------------\n"
        readme_text += "\n"
        readme_text += readme_variables_text + "\n"
        readme_text += "\n"

    readme_dependencies_text = readme_dependencies_text.strip()
    if len(readme_dependencies_text) > 0:
        readme_text += "Dependencies\n"
        readme_text += "--------------\n"
        readme_text += "\n"
        readme_text += readme_dependencies_text + "\n"
        readme_text += "\n"

    readme_text += "Example Playbook\n"
    readme_text += "--------------\n"
    readme_text += "\n"
    readme_text += "```yaml\n"
    readme_text += "- hosts: servers\n"
    readme_text += "  roles:\n"
    readme_text += "    - role: " + role_name + "\n"
    readme_text += "```\n"
    readme_text += "\n"

    readme_license_text = readme_license_text.strip()
    if len(readme_license_text) > 0:
        readme_text += "License\n"
        readme_text += "--------------\n"
        readme_text += "\n"
        readme_text += readme_license_text + " License"
        if readme_license_text == 'Apache':
            readme_text += " 2.0"
        readme_text += "\n"

    with open(ROLE_ROOT + DS + 'README.md', mode='w') as f:
        f.write(readme_text)

    print(readme_text)
