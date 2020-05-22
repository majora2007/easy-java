"""
Run SQL in TOAD, export to txt file with | as deliminator. 
Then feed into python script and give it a name for the entity. 
It will then spit out a Entity.java, EntityRowMapper.java and optional typescript.
"""
import re
import os

from gooey import Gooey, GooeyParser

from parse import DataParser
from generator import Generator

def get_argument(argument, default="None"):
	if argument:
		return argument[0]
	else:
		return default

def init_args():

    parser = GooeyParser(description='Enter the name of the POJO in Entity and select a file with pipe separated (|) values with included headers. Click typescript for typescript generation.')
    # Required Parameters
    parser.add_argument('--entity', required=True, nargs=1, metavar='Entity Name', help='Name of the Entity')
    parser.add_argument('--data', required=True, nargs=1, metavar='Data', help='Pipe separated values as result of query', widget='FileChooser')

    # Optional
    parser.add_argument('--typescript', required=False, metavar='Typescript', action='store_true', help="Generate typescript")

    return parser.parse_args()


@Gooey
def main(program_name='Easy Java', program_description='Generate POJOs and Row Mappers from data output'):
    args = init_args()
    entity = str(get_argument(args.entity))
    data_file = str(get_argument(args.data))

    gen = Generator()
    gen.load_file(data_file)
    gen.generate_entity_files(entity, os.getcwd(), bool(args.typescript))


if __name__ == '__main__':
    main()
