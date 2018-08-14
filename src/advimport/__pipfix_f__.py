import subprocess
import re
from sys import version_info


def pipfix_f(module, askconfirm=True, automate_install=True):

    search_res = str(subprocess.run(['pip', 'search', module], stdout=subprocess.PIPE).stdout.decode('utf-8'))

    if search_res != "":
        pip_search_results = []
        for item in search_res.split("\n"):
            try:
                pkgname = re.search(r"^((\w+-*_*)+)", item).group()
                pkgversion = re.search(r"\((\d+|(\d+\.\d*)+)\)", item).group().replace("(", '').replace(")", '')
                if module in pkgname:
                    pip_search_results.append((pkgname, pkgversion))
            except:
                pass

        if len(pip_search_results) != 0:
            if automate_install is False:
                print("-- Pip Search results --")
                for item in pip_search_results:
                    print(pip_search_results.index(item), item[0])
                    #  print the module name and its position in the result list
                try:
                    user_choice = int(input("Option ({0} -> {1}): ".format(0, len(pip_search_results)-1)) )
                    if user_choice not in range(0, len(pip_search_results)):
                        print("Choice", user_choice, "not in index. Aborting")
                        return False
                    chosen_package = pip_search_results[user_choice][0]
                except ValueError:
                        print("Not an integer. Aborting")
                        return False
            else:  # if automateinstall is True
                chosen_package = pip_search_results[0][0]
                print("Automatically selected", chosen_package, "for installation")
            #  in both cases, if a matching package has been found
            print("Trying to install", chosen_package, "using pip" + str(version_info[0]))
            if askconfirm:
                if input("Proceed? y/n: ") == "y":
                    pass
                else:
                    print("Aborted")
                    return False
            # install the package using pip
            if shell("pip" + str(version_info[0]) + " install --user " + chosen_package) == 0:
                print("Module", chosen_package, "should be installed. Re-run the script to apply")
                return True
            else:
                print("An error occurred while trying to install", chosen_package + ". Aborting")
                return False

        else:  # if no item in pip_search_results
            print("No modules found. Aborting")
            return False

    else:  # if pip couldn't find the word even in the description
        print("No modules found. Aborting")
        return False
