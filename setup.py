from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('spydf.pyw', base=base, icon="icon.ico")
]

setup(name='SPYDF',
      version = '2.0',
      description = 'Automatically converts your screenshots into PDF',
      options = {'build_exe': build_options},
      executables = executables)
