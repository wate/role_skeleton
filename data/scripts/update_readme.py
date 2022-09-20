#!/usr/bin/env python
from ensurepip import version
import os
import re
import yaml

DS = os.sep
ROLE_ROOT = os.path.dirname(os.path.dirname(__file__))

def parse_meta_file():
    role_info = {
        'name': os.path.basename(ROLE_ROOT),
        'description': None,
        'platforms': {},
        'license': None,
        'dependencies': []
    }
    if os.path.exists(ROLE_ROOT + DS + 'meta' + DS + 'main.yml'):
        role_meta = yaml.safe_load(
            open(ROLE_ROOT + DS + 'meta' + DS + 'main.yml', 'r'))
        meta_keys = role_meta.keys()
        if 'galaxy_info' in meta_keys:
            galaxy_info_keys = role_meta['galaxy_info'].keys()
            if 'role_name' in galaxy_info_keys:
                role_info['name'] = role_meta['galaxy_info']['role_name']
            if 'description' in galaxy_info_keys:
                role_info['description'] = role_meta['galaxy_info']['description']
            if 'license' in galaxy_info_keys:
                role_info['license'] = role_meta['galaxy_info']['license']
            if 'platforms' in galaxy_info_keys:
                platforms = {}
                for platform in  role_meta['galaxy_info']['platforms']:
                    platform_name = platform['name']
                    platforms[platform_name] = []
                    if 'versions' in platform.keys() and 'all' not in platform['versions']:
                        platforms[platform_name] = []
                        for platform_version in platform['versions']:
                            platforms[platform_name].append(platform_version)
                role_info['platforms'] = platforms
        if 'dependencies' in role_meta.keys():
            role_info['dependencies'] = []
            for dependency in role_meta['dependencies']:
                if dependency is str:
                    role_info['dependencies'].append(dependency)
                else:
                    dependency_keys = dependency.keys()
                    if 'role' in dependency_keys:
                        role_info['dependencies'].append(dependency['role'])
                    elif 'name' in dependency_keys:
                        role_info['dependencies'].append(dependency['name'])
                    elif 'src' in dependency_keys:
                        role_info['dependencies'].append(dependency['src'])

    return role_info

def parse_var_file():
    var_docs = {}
    if os.path.exists(ROLE_ROOT + DS + 'defaults' + DS + 'main.yml'):
        with open(ROLE_ROOT + DS + 'defaults' + DS + 'main.yml') as fp:
            var_name = None
            doc_block_start = False
            doc_block_end = False
            doc_block_lines = []
            for line in fp.readlines():
                if len(line.strip()) > 0:
                    var_name_match = re.search(r'^([a-zA-Z0-9_]+)\s?:\s+', line)
                    if var_name_match:
                        var_name = var_name_match.group(1)
                    else:
                        doc_block_sep_match = re.search(r'^#\s+-{3,}', line)
                        if doc_block_sep_match:
                            if doc_block_start:
                                doc_block_end = True
                            else:
                                doc_block_start = True
                        else:
                            doc_block_match = re.search(r'^#\s+(.+)', line)
                            if doc_block_match and doc_block_start and not doc_block_end:
                                doc_block_lines.append(doc_block_match.group(1).strip())

                    if var_name:
                        var_docs[var_name] = "  \n".join(doc_block_lines)
                        var_name = None
                        doc_block_start = False
                        doc_block_end = False
                        doc_block_lines = []
                else:
                    var_name = None
                    doc_block_start = False
                    doc_block_end = False
                    doc_block_lines = []

    return var_docs

if os.path.exists(ROLE_ROOT + DS + 'README.md'):
    role_info = parse_meta_file()
    var_docs = parse_var_file()

    # Readmeのテキストを生成
    readme_text = role_info['name'] + "\n"
    readme_text += "=================\n"
    readme_text += "\n"
    if role_info['description']:
        readme_text += role_info['description'] + "\n"
        readme_text += "\n"

    if len(role_info['platforms']) > 0:
        readme_text += "OS Platform\n"
        readme_text += "-----------------\n"
        readme_text += "\n"
        for platform_name, platform_versions in role_info['platforms'].items():
            readme_text += '### ' + platform_name + "\n"
            readme_text += "\n"
            if len(platform_versions) > 0:
                readme_text += "\n".join(map(lambda version: '- ' + str(version), platform_versions)) + "\n"
                readme_text += "\n"

    if len(var_docs) > 0:
        readme_text += "Role Variables\n"
        readme_text += "--------------\n"
        readme_text += "\n"
        for var_name, var_doc in var_docs.items():
            readme_text += '### `' + var_name + "`\n"
            readme_text += "\n"
            if len(var_doc) > 0:
                readme_text += var_doc.strip()+ "\n"
                readme_text += "\n"

    if len(role_info['dependencies']) > 0:
        readme_text += "Dependencies\n"
        readme_text += "--------------\n"
        readme_text += "\n"
        readme_text += "\n".join(map(lambda dependency: "- " + dependency, role_info['dependencies']))
        readme_text += "\n"
    readme_text += "Example Playbook\n"
    readme_text += "--------------\n"
    readme_text += "\n"
    readme_text += "```yaml\n"
    readme_text += "- hosts: servers\n"
    readme_text += "  roles:\n"
    readme_text += "    - role: " + role_info['name'] + "\n"
    readme_text += "```\n"
    readme_text += "\n"
    if role_info['license']:
        readme_text += "License\n"
        readme_text += "--------------\n"
        readme_text += "\n"
        readme_text += role_info['license'] + " License"
        if role_info['license'] == 'Apache':
            readme_text += " 2.0"
        readme_text += "\n"

    with open(ROLE_ROOT + DS + 'README.md', mode='w') as f:
        f.write(readme_text)

    print(readme_text)
