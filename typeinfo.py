from util import first_upper

class TypeInfo(object):
    var_type = ''
    var_name = ''
    sql_var = ''

    def __init__(self, var_type, var_name, sql_var):
        self.var_name = var_name
        self.var_type = var_type
        self.sql_var = sql_var
    
    def generate_definitition(self):
        return '\tprivate ' + self.var_type + ' ' + self.var_name + ';'
    
    def generate_getter(self):
        return '\tpublic ' + self.var_type + ' get' + first_upper(self.var_name) +  '() {\n\t\treturn this.' + self.var_name + ';\n\t}'
    
    def generate_setter(self):
        return '\tpublic void set' + first_upper(self.var_name) +  '(' + self.var_type + ' ' + self.var_name + ') {\n\t\tthis.' + self.var_name + ' = ' + self.var_name + ';\n\t}'
    
    def generate_rowmap_method(self):
        return '.set' + first_upper(self.var_name) + '(rs.get' + first_upper(self.var_type) + '("' + self.sql_var + '"));'
    
    def generate_ts_definition(self):
        ts_type = 'any'
        if self.var_type == 'int':
            ts_type = 'number'
        elif self.var_type == 'float':
            ts_type = 'number'
        elif self.var_type == 'boolean':
            ts_type = 'boolean'
        elif self.var_type == 'String':
            ts_type = 'string'
        
        return self.var_name + ': ' + ts_type + ';'
