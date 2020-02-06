import sys
import os
import argparse




# python test.py -p 8888 --host=localhost -d .

# print('\n******************************************')
# print("This is the name of the script: ", sys.argv[0])
# print("Number of arguments: ", len(sys.argv))
# print("The arguments are: ", str(sys.argv))
# print('******************************************\n')

parser = argparse.ArgumentParser(description='Start local json server.')
parser.add_argument('-b', '--bind', default='127.0.0.1:8888', help='Bind server address and port.')
parser.add_argument('-w', '--watch', default='db.json')
args = parser.parse_args()

address = args.bind
filename = args.watch

# Console.write('White string', 'white')
# Console.write('Yellow string', 'yellow')
# Console.write('Bold Yellow string', 'yellow', bold=True)


# if not os.path.exists(filename):
#     pass

# print('\n***************************')
# print(f'Address is {address}')
# print(f'Data file is {filename}')
# print('***************************\n')
