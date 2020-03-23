import base64
import hashlib
import re
from   typing  import List, Optional, Tuple

# <https://discuss.python.org/t/identifying-parsing-binary-extension-filenames/>
MODULE_EXT_RGX = re.compile(
    r'(?<=.)(?:\.(?:py|so)|\.[-A-Za-z0-9_]+\.(?:pyd|so))\Z'
)

DIST_INFO_DIR_RGX = re.compile(
    r'[A-Za-z0-9](?:[A-Za-z0-9._]*[A-Za-z0-9])?-[A-Za-z0-9_.!+]+\.dist-info'
)

DATA_DIR_RGX = re.compile(
    r'[A-Za-z0-9](?:[A-Za-z0-9._]*[A-Za-z0-9])?-[A-Za-z0-9_.!+]+\.data'
)

def comma_split(s: str) -> List[str]:
    """
    Split apart a string on commas, discarding leading & trailing whitespace
    from all parts and discarding empty parts
    """
    return [k for k in map(str.strip, s.split(',')) if k]

def bytes_signature(b: bytes) -> Tuple[int, str]:
    return (
        len(b),
        'sha256=' + urlsafe_b64encode_nopad(hashlib.sha256(b).digest()),
    )

def urlsafe_b64encode_nopad(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('us-ascii')

def pymodule_basename(filename: str) -> Optional[str]:
    """
    If ``filename`` (a filename without any directory components) has a file
    extension indicating it is a Python module (either source or binary
    extension), return the part before the extension; otherwise, return `None`.
    """
    m = MODULE_EXT_RGX.search(filename)
    if m is not None:
        return filename[:m.start()]
    else:
        return None

def is_dist_info_dir(name: str) -> bool:
    return DIST_INFO_DIR_RGX.fullmatch(name) is not None

def is_data_dir(name: str) -> bool:
    return DATA_DIR_RGX.fullmatch(name) is not None
