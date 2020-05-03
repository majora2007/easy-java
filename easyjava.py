"""
Run SQL in TOAD, export to txt file with | as deliminator. 
Then feed into python script and give it a name for the entity. 
It will then spit out a Entity.java, EntityRowMapper.java and optional typescript.
"""
import argparse
import re
import os

import parse as parse
from typeinfo import TypeInfo
from util import camel_case, first_upper, first_chars, spinal_case, pyinstaller_get_full_path

def get_argument(argument, default="None"):
	if argument:
		return argument[0]
	else:
		return default

def init_args():
    parser = argparse.ArgumentParser()
    # Required Parameters
    parser.add_argument('--entity', required=True, nargs=1, help="Name of the Entity")
    parser.add_argument('--data', required=False, nargs=1, help="Pipe separated values (.txt) as result of query")

    # Optional
    parser.add_argument('--typescript', required=False, action='store_true', help="If supplied, will output a typescript file as well for Entity")

    return parser.parse_args()

def parse_data(data_file):
    types = []
    lines = []
    with open(data_file, 'r') as in_file:
        lines = in_file.read().splitlines() 
    

    header = lines[0].split('|')
    print(header)

    line_data = lines[1].split('|')
    for idx, cell in enumerate(line_data):
        types.append(TypeInfo(parse.parse_type(cell, header[idx]), camel_case(header[idx]), header[idx]))
    
    return types

def generate_entity_file(entity_name, types):
    print('Generating {0}.java'.format(entity_name))    

    declarations = ''
    for t in types:
        declarations = declarations + t.generate_definitition() + '\n'
    
    getter_setter = '\n'
    for t in types:
        getter_setter = getter_setter + t.generate_getter() + '\n' + t.generate_setter() + '\n'
    
    to_string = '" ' + entity_name + ' ['

    for t in types:
        # "[%ENTITY%] [[%VARIABLE%]=" + [%VARIABLE%] + ", Name=" + name + ", Designation=" + designation + ", Salary=" + salary + "]";
        to_string = to_string + t.var_name + '= " + ' + t.var_name + ' + ", '
    to_string = ''.join(to_string[:len(to_string)-3]) + '"]";'
    
    template = ''
    path = pyinstaller_get_full_path('templates/Entity.java') #os.path.abspath(os.path.join(os.getcwd(), 'templates/Entity.java')) # Local only

    with open(path, 'r') as in_file:
        template = in_file.read()

    template = template.replace('[%ENTITY%]', first_upper(entity_name)).replace('[%DECLARATION%]', declarations).replace('[%GETTER_SETTER%]', getter_setter).replace('[%TOSTRING%]', to_string)
    with open(first_upper(entity_name) + '.java', 'w+') as out_file:
        out_file.write(template)

def generate_entity_row_mapper(entity_name, types):
    print('Generating {0}RowMapper.java'.format(entity_name))   

    template = ''
    path = pyinstaller_get_full_path('templates/EntityRowMapper.java') # os.path.abspath(os.path.join(os.getcwd(), 'templates/EntityRowMapper.java')) # Local only

    with open(path, 'r') as in_file:
        template = in_file.read()
    
    entity_var_name = first_chars(entity_name)

    row_maps = ''
    for t in types:
        row_maps = row_maps + '\t\t' + entity_var_name + t.generate_rowmap_method() + '\n'
    
    template = template.replace('[%ENTITY%]', first_upper(entity_name)).replace('[%ENTITYVAR%]', entity_var_name).replace('[%ROWMAPPER%]', row_maps)
    
    with open(first_upper(entity_name) + 'RowMapper.java', 'w+') as out_file:
        out_file.write(template)

def generate_entity_typescript(entity_name, types):
    print('Generating {0}.ts'.format(spinal_case(entity_name).lower()))   

    template = ''
    path = pyinstaller_get_full_path('templates/entity.ts') # os.path.abspath(os.path.join(os.getcwd(), 'templates/entity.ts')) # Local only
    with open(path, 'r') as in_file:
        template = in_file.read()

    definitions = ''
    for t in types:
        definitions = definitions + '  ' + t.generate_ts_definition() + '\n'
    
    template = template.replace('[%ENTITY%]', first_upper(entity_name)).replace('[%DEFINITIONS%]', definitions)
    
    with open(spinal_case(entity_name).lower() + '.ts', 'w+') as out_file:
        out_file.write(template)

if __name__ == '__main__':
    args = init_args()
    entity = str(get_argument(args.entity))
    data_file = str(get_argument(args.data))

    print('Enity: {0}'.format(entity))
    

    root_dir = os.getcwd()
    types = parse_data(data_file)

    generate_entity_file(entity, types)
    generate_entity_row_mapper(entity, types)

    if bool(args.typescript):
        generate_entity_typescript(entity, types)
