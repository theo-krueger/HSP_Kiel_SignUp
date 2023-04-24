import sys
import subprocess
import pkg_resources

from gui_version import interface
import signup


def setup():
    required = {'selenium'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        print("A module is missing. Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)


if __name__ == "__main__":
    setup()

    interface.Windows().mainloop()
    print(interface.user_input_dic)

    signup.signup(interface.user_input_dic)
