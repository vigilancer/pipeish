# vim: set ts=4 sw=4 st=4 et:

import shlex
# from subprocess import DEVNULL, PIPE, STDOUT, Popen
import subprocess
import sys


class Environment:
    pass


class Shell:

    def __init__(self, env=Environment(), check=True, *args):
        self.env = env
        self.check = check

    def __call__(self, *args):
        if len(args) == 0:
            return

        self.cmds = args

        # maybe it's single string with pipes
        if len(self.cmds) == 1:
            self.cmds = [c.strip() for c in self.cmds[0].split('|') if c]

        if len(self.cmds) == 1:
            self.__exec_single()
        else:
            self.__exec_multiple()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self.check and self.retcode is not 0:
            sys.exit(self.retcode)

    def __exec_multiple(self):
        proc = subprocess.Popen(
            shlex.split(self.cmds[0]),
            stdout=subprocess.PIPE,
        )
        self.retcode = proc.returncode

        for cmd in self.cmds[1:-1]:
            proc = subprocess.Popen(
                shlex.split(cmd),
                stdin=proc.stdout,
                stdout=subprocess.PIPE,
            )
            self.retcode = proc.returncode

        proc = subprocess.Popen(
            shlex.split(self.cmds[-1]),
            stdin=proc.stdout,
        )
        proc.wait()
        self.retcode = proc.returncode

    def __exec_single(self):
        p = subprocess.run(shlex.split(self.cmds[0]))
        self.retcode = p.returncode
