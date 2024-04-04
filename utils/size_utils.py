import os

def get_size(path):
    total_size = 0
    if os.path.isfile(path):
        total_size = os.path.getsize(path)
    else:
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
    return total_size

def convert_size(size_bytes):
    if size_bytes >= 1073741824:
        size_gb = size_bytes / 1073741824
        return f"{size_gb:.2f} GB"
    elif size_bytes >= 1048576:
        size_mb = size_bytes / 1048576
        return f"{size_mb:.2f} MB"
    else:
        return f"{size_bytes} bytes"