import os
import subprocess


class SetLanguage:
    @staticmethod
    def powershell_language_script():
        path = os.path.dirname(os.path.abspath(__file__)) + "\\"
        result = subprocess.run([r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe',
                                 path + "Change_default_language.ps1"],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        return result
