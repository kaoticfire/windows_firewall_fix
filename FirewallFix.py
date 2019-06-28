#  !/usr/bin/bash/python3
#  Copyright (c) 2019.
#  Author: 'Virgil Hoover'

__version__ = '1.0'

from os import getenv, remove, system, name
from os.path import isfile
from subprocess import DEVNULL, call


def check_admin():
    """ Check if the user running this has admin rights """
    try:
        temp_file = getenv('SystemRoot') + '/System32/temp.txt'
        access = 'a'
        with open(temp_file, access) as temp:
            temp.write('This is a test')
        if temp_file:
            remove(temp_file)
    except IOError:
        print('An error occurred while checking admin rights.')


def delete_rule(rule):
    """ Remove broken rules from Windows Firewall """
    call(f'netsh advfirewall firewall delete rule name="{rule}"', stderr=DEVNULL)


def add_rule(rule, file_path):
    """ Add rules to Windows Firewall """
    protos = ('tcp', 'udp')
    for i in protos:
        call(
            f'netsh advfirewall firewall add rule name="{rule}" '
            f'dir=in action=allow protocol={i} program="{file_path}" enable=yes', stdout=DEVNULL)
        print(f'Rule {rule} for {file_path} added for all {i} port protocols.')


def main():
    if name == 'nt':
        check_admin()
        condition = True
        while condition:
            print('This program allows a user with admin rights to rebuild a Windows Firewall Rule.')
            print()
            rule_name = input('What is the name of the firewall Rule, you wish to rebuild? ')
            delete_rule(rule_name)
            path_to_file = input('Where does the application reside? ')
            exists = isfile(path_to_file)
            if exists:
                add_rule(rule_name, path_to_file)
                condition = False
            else:
                print("I'm sorry but that does not appear to be a valid application.")
                _ = system('cls')
        _ = system('pause')


if __name__ == '__main__':
    main()
