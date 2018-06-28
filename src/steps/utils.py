import threading
import subprocess
import os

def get_abs_path(relative_path):
    return os.path.abspath(relative_path)

def get_prev_dir(path):
    return '/'.join(path.split('/')[:-1])

def get_sibling_dir(dir_path, sibling_dir_name):
    return '{}/{}'.format(get_prev_dir(dir_path), sibling_dir_name)

def _call(popen_args, callback, stdout=None):
    def runInThread(popen_args, callback):
        proc = subprocess.Popen(*popen_args, stdout=stdout)
        proc.wait()
        callback()
        return
    thread = threading.Thread(target=runInThread, args=(popen_args, callback))
    thread.start()
    return thread

def call(command, stdout=None):
    event = threading.Event()
    _call([command.split()], callback=event.set, stdout=stdout)
    event.wait()

def call_background(command, stdout=None):
    _call([command.split()], callback=lambda: None, stdout=stdout)

__all__ = ['call', 'call_background']
