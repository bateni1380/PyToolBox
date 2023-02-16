from typing import Any, Callable, Dict, Iterable, List, Literal, Tuple


class VersionController:
    '''
        This class is a version controller like github.
            First of all, you make an instance of the object (vc = VersionController())
            Next you can add variables to vc by adding parameters (vc.x = 100)
            After applying changes, you should use vc.make_check_point() function to save changes.
            Whenever you needed to change version, you can use vc.undo() and vc.redo() functions.
                the parameters of the VersionController object are sync with the version.
            You can use vc.print_verssions() to see all versions variables together.
    '''

    def __init__(self):
        '''
        You don't need to pass anything to the constructor.
        '''
        self.__version_num: int = 0
        self.__history: List[Dict] = [{}]

    def make_check_point(self):
        '''
            After you changed VersionController variables (vs.a, vc.b, ...) you must use this
            function in order to commit changes.
        '''
        # Erase checkpoints after this checkpoint (as we don't remember every branch.)
        while self.__version_num+1 < len(self.__history):
            self.__history.pop()

        self_vars = {name: vars(self)[name] for name in vars(
            self) if not name.startswith('_')}

        # Make a dictionary (based on the variables that exist in current instance)
        base_version = self.__make_version()

        # Append the version to end of our history (current version is the last as we have deleted the remaining part's of history)
        self.__history.append(base_version)

        # Change the version and update the class parameters
        self.__change_version(self.__version_num, self.__version_num+1)

    def undo(self):
        '''
            Use this if you want to get back to variables of last commit.
        '''
        if self.__version_num == 0:
            raise Exception("First checkpoint!")
        self.__change_version(self.__version_num, self.__version_num-1)

    def redo(self):
        '''
            Use this if you have used undo function and you want to get back to the version before undo.
        '''
        if self.__version_num+1 == len(self.__history):
            raise Exception("Last checkpoint!")
        self.__change_version(self.__version_num, self.__version_num+1)

    def print_versions(self):
        '''
            This function prints all versions and their variables.
        '''
        for i in range(len(self.__history)):
            if i == self.__version_num:
                print('+', end='')
            print('version {}: {}'.format(i, self.__history[i]))

    def __make_version(self):
        base_version = {}

        for key in vars(self):
            if not key.startswith('_'):
                att = getattr(self, key)
                if hasattr(att, 'copy'):
                    att = att.copy()
                base_version[key] = att

        return base_version

    def __change_version(self, base_version_num: int, version_num: int):
        for key in self.__history[base_version_num]:
            if key not in self.__history[version_num]:
                delattr(self, key)

        for key in self.__history[version_num]:
            value = self.__history[version_num][key]
            setattr(self, key, value)

        self.__version_num = version_num
