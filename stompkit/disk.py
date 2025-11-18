import os
import collections
import ctypes
import sys
import locale
import string

from stompkit.progress import progress_bar

locale.setlocale(locale.LC_ALL, '')

PULARGE_INTEGER = ctypes.POINTER(ctypes.c_ulonglong)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
kernel32.GetDiskFreeSpaceExW.argtypes = (ctypes.c_wchar_p,) + (PULARGE_INTEGER,) * 3

class UsageTuple(collections.namedtuple('UsageTuple', 'drive, total, used, free')):
    def __str__(self):
        _p_used = f"{(self.used / self.total)*100:0.2f}"
        _p_free = f"{100.0 - float(_p_used):0.2f}"
        _output = [
            f"<{self.__class__.__name__}> Disk {self.drive}",
            f"Total: {self.total:n}",
            f" Used: {self.used:n} ({_p_used}%)",
            f" Free: {self.free:n} ({_p_free}%)",
            progress_bar(float(_p_used))
        ]
        return "\n\t".join(_output)
    def __repr__(self):
        return self.__class__.__name__ + '(drive={:s}, total={:n}, used={:n}, free={:n})'.format(*self)

def get_drives():
    drives = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives

def raise_disk_usage_error(error_code, path):
    windows_error_message = ctypes.FormatError(error_code)
    raise ctypes.WinError(error_code, '{} {!r}'.format(windows_error_message, path))

def calculate_disk_usage(path):
    try:
        path = os.fsdecode(path)
    except AttributeError:
        pass
    _, total, free = ctypes.c_ulonglong(), ctypes.c_ulonglong(), ctypes.c_ulonglong()
    success = kernel32.GetDiskFreeSpaceExW(path, ctypes.byref(_), ctypes.byref(total), ctypes.byref(free))
    if not success:
        raise_disk_usage_error(ctypes.get_last_error(), path)
    used = total.value - free.value
    return UsageTuple(path, total.value, used, free.value)

def get_system_disk_usage():
    drives = get_drives()
    disk_usage = [calculate_disk_usage(f"{drive}:/") for drive in drives]
    for disk in disk_usage:
        print(disk)