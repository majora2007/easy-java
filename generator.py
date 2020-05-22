""" Resposible for generating code related to a language """
import os

from parse import DataParser
from util import camel_case, first_upper, first_chars, spinal_case, pyinstaller_get_full_path
from languagetype import Language

DEFINITION_TEMPLATE = '\tprivate {0} {1};'
GETTER_TEMPLATE = '\tpublic {0} get{1}() {{\n\t\treturn this.{2};\n\t}}'
SETTER_TEMPLATE = '\tpublic void set{0}({1} {2}) {{\n\t\tthis.{2} = {2};\n\t}}'
TOSTRING_TEMPLATE = '"[{0}] [{1}]"'
TOSTRING_INNER_TEMPLATE = '{}=" + {} + "'
ROWMAP_SETTER_TEMPLATE = '\t\t{0}.set{1}(rs.get{1}("{2}"));'
TYPESCRIPT_DEFINITION_TEMPLATE = '  {0}: {1};'


class Generator(object):
    data = []
    types = {}

    def __init__(self):
        self.parser = DataParser()


    def load_file(self, data_file):
        # Reset information about a file
        self.data = []
        self.types = {}

        with open(data_file, 'r') as in_file:
            lines = in_file.read().splitlines() 
    

        header = lines[0].split('|')
        print(header)

        for item in header:
            self.types[item] = None

        line_data = []
        for line in lines[1:]:
            line_data = [c for c in line.split('|') if c != '' and c != ' ']
            if len(line_data) is len(lines[0]):
                break # TODO: Is there a better way to handle this? 
        
        for idx, cell in enumerate(line_data):
            self.types[header[idx]] = self.parser.parse_type(cell), camel_case(header[idx])
        
        print(self.types) # TODO: Pretty print the mappings to the console
    
    def generate_entity_files(self, entity_name, folder_path, create_typescript=False):
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        
        self._make_bean(entity_name, folder_path)
        self._make_bean_rowmapper(entity_name, folder_path)
        if create_typescript:
            self._make_typescript(entity_name, folder_path)
    
    def _make_bean(self, entity_name, folder_path):
        if not entity_name[0].isupper():
            entity_name = first_upper(entity_name)

        print('Generating {0}.java'.format(entity_name))

        declarations = '\n'.join(self._generate_definitions())
        getter_setter = '\n'.join(self._generate_getters_setters())
        to_string = self._generate_tostring(entity_name)
        
        template = ''
        path = pyinstaller_get_full_path('templates/Entity.java')

        with open(path, 'r') as in_file:
            template = in_file.read()

        template = template.replace('[%ENTITY%]', entity_name).replace('[%DECLARATION%]', declarations).replace('[%GETTER_SETTER%]', getter_setter).replace('[%TOSTRING%]', to_string)
        
        output_path = os.path.join(folder_path, entity_name + '.java')
        
        with open(output_path, 'w+') as out_file:
            out_file.write(template)
    
    def _make_bean_rowmapper(self, entity_name, folder_path):
        if not entity_name[0].isupper():
            entity_name = first_upper(entity_name)

        print('Generating {0}RowMapper.java'.format(entity_name))

        template = ''
        path = pyinstaller_get_full_path('templates/EntityRowMapper.java')

        with open(path, 'r') as in_file:
            template = in_file.read()
        
        row_maps = '\n'.join(self._generate_rowmap(entity_name))
        
        template = template.replace('[%ENTITY%]', first_upper(entity_name)).replace('[%ENTITYVAR%]', first_chars(entity_name)).replace('[%ROWMAPPER%]', row_maps)
        output_path = os.path.join(folder_path, entity_name + 'RowMapper.java')
        
        with open(output_path, 'w+') as out_file:
            out_file.write(template)
    
    def _make_typescript(self, entity_name, folder_path):
        print('Generating {0}.ts'.format(spinal_case(entity_name).lower()))   

        template = ''
        path = pyinstaller_get_full_path('templates/entity.ts')
        with open(path, 'r') as in_file:
            template = in_file.read()

        definitions = '\n'.join(self._generate_typescript_definitions())
        
        template = template.replace('[%ENTITY%]', first_upper(entity_name)).replace('[%DEFINITIONS%]', definitions)
        output_path = os.path.join(folder_path, spinal_case(entity_name).lower() + '.ts')

        with open(output_path, 'w+') as out_file:
            out_file.write(template)
    
    def _generate_typescript_definitions(self):
        code_lines = []
        for key in self.types:
            var = self.types[key]
            code_lines.append(TYPESCRIPT_DEFINITION_TEMPLATE.format(var[1], self.parser.translate_type(var[0], Language.Typescript)))
        return code_lines
    
    def _generate_rowmap(self, entity_name):
        entity_var_name = first_chars(entity_name)

        code_lines = []
        for key in self.types:
            var = self.types[key]
            code_lines.append(ROWMAP_SETTER_TEMPLATE.format(entity_var_name, first_upper(var[1]), key))
        return code_lines
    
    def _generate_getters_setters(self):
        code_lines = []
        for key in self.types:
            var = self.types[key]
            java_type = self.parser.translate_type(var[0], Language.Java)
            print('GETTER: Type for {0}: {1}'.format(var[1], java_type))
            code_lines.append(GETTER_TEMPLATE.format(java_type, first_upper(var[1]), var[1]))
            code_lines.append(SETTER_TEMPLATE.format(first_upper(java_type), java_type,  var[1]))
        return code_lines

    def _generate_definitions(self):
        code_lines = []
        for key in self.types:
            var = self.types[key]
            code_lines.append(DEFINITION_TEMPLATE.format(self.parser.translate_type(var[0], Language.Java), var[1]))
        print(code_lines)
        return code_lines

    def _generate_tostring(self, entity_name):
        variables = []
        for key in self.types:
            var = self.types[key]
            variables.append(first_upper(var[1]))
            variables.append(var[1])
        inner_format_templates = ', '.join([TOSTRING_INNER_TEMPLATE] * len(self.types.keys()))
        return TOSTRING_TEMPLATE.format(entity_name, inner_format_templates.format(*variables))