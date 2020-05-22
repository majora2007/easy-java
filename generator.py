""" Resposible for generating code related to a language """
import os

from parse import DataParser
from util import camel_case, first_upper, first_chars, spinal_case, pyinstaller_get_full_path

DEFINITION_TEMPLATE = '\tprivate {0} {1};'
GETTER_TEMPLATE = '\tpublic {0} get{1}() {{\n\t\treturn this.{2};\n\t}}'
SETTER_TEMPLATE = '\tpublic void set{0}({1} {2}) {{\n\t\tthis.{2} = {2};\n\t}}'
TOSTRING_TEMPLATE = '"[{0}] [{1}]"'
TOSTRING_INNER_TEMPLATE = '{}=" + {} + "'

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
        
        # {'ACTIONITEMIMPACTID': ('int', 'actionItemImpactId'), 'ACTIONITEMID': ('int', 'actionItemId'), 'APPID': ('int', 'appId'), 'APPNAME': (None, 'appName'), 'UPDATEDBY': ('String', 'updatedBy'), 'LASTUPDATED': ('String', 'lastUpdated'), 'DISTANCE': ('float', 'distance')}
        print(self.types)
    
    def generate_entity_files(self, entity_name, folder_path):
        if not os.path.isdir(folder_path):
            # Create folder
            os.mkdir(folder_path)
        
        # Make Bean
        self._make_bean(entity_name, folder_path)
    
    def _make_bean(self, entity_name, folder_path):
        if not entity_name[0].isupper():
            entity_name = first_upper(entity_name)

        print('Generating {0}.java'.format(entity_name))

        declarations = '\n'.join(self._generate_definitions())
        
        getter_setter = '\n'.join(self._generate_getters_setters())

        to_string = self._generate_tostring(entity_name)
        
        
        #to_string = '" ' + entity_name + ' ['

        
        #for t in types:
            # "[%ENTITY%] [[%VARIABLE%]=" + [%VARIABLE%] + ", Name=" + name + ", Designation=" + designation + ", Salary=" + salary + "]";
        #    to_string = to_string + t.var_name + '= " + ' + t.var_name + ' + ", '
        #to_string = ''.join(to_string[:len(to_string)-3]) + '"]";' 
        
        template = ''
        path = pyinstaller_get_full_path('templates/Entity.java')

        with open(path, 'r') as in_file:
            template = in_file.read()

        template = template.replace('[%ENTITY%]', entity_name).replace('[%DECLARATION%]', declarations).replace('[%GETTER_SETTER%]', getter_setter).replace('[%TOSTRING%]', to_string)
        
        output_path = os.path.join(folder_path, entity_name + '.java')
        
        with open(output_path, 'w+') as out_file:
            out_file.write(template)
    
    def _generate_getters_setters(self):
        code_lines = []
        for key in self.types:
            var = self.types[key]
            code_lines.append(GETTER_TEMPLATE.format(var[0], first_upper(var[1]), var[1]))
            code_lines.append(SETTER_TEMPLATE.format(var[0], first_upper(var[1]), var[1]))
        print(code_lines)
        return code_lines

    def _generate_definitions(self):
        code_lines = []
        for key in self.types:
            var = self.types[key]
            code_lines.append(DEFINITION_TEMPLATE.format(var[0], var[1]))
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