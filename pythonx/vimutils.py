import os
import vim


def vimrepr(obj):
    """
    turn `obj` into corresponding vim representation.
    since `obj` needs to be correspond to vimscript data structure,
    only following datatype is allowed:
        int
        float
        str
        list
        dict
    otherwise, a TypeError will be raised.
    """
    if isinstance(obj, (int, float)):
        return str(obj)
    elif isinstance(obj, str):
        return "'{}'".format(obj.replace("'", "''"))
        # turn str into vim string literal
    elif isinstance(obj, list):
        return "[{}]".format(', '.join(map(vimrepr, obj)))
    elif isinstance(obj, dict):
        return "{%s}" % ''.join('{}: {}, '.format(vimrepr(k), vimrepr(v))
                                for k, v in obj.items())
    else:
        raise TypeError(
            'this type can\'t be converted: {}'.format(
                type(obj).__name__))


def let_vimrepr(varname, obj):
    """
    pass back the obj into vimscript in given variable name `varname`.
    """
    vim.command('let {} = {}'.format(varname, vimrepr(obj)))


def raw_textrepr(text):
    """
    command receive raw text as input. however, it needs to escape first.
    for example:
        :!touch a\ b " create a file named 'a b'
        :e a\ b      " however ':e a b' won't work
    """
    return text.replace(' ', r'\ ').replace('"', r'\"').replace("'", r"\'")


def target_exists(name, typ=None):
    """
    check if the target file(in general sense) exists in cwd or its acenstors.
    search will stop when reaching the root.
    typ refers to the specific type of name:
        None:   not specific
        'f':    normal file
        'd':    directory
    return the full path of the file is found, None if not.
    """
    predicate = {
        None: os.path.exists,
        'f': os.path.isfile,
        'd': os.path.isdir
    }[typ]
    path = os.path.abspath(os.getcwd())
    while(os.path.dirname(path) != path):
        if (any(os.path.basename(p) == name
                for p in os.listdir(path) if predicate(p))):
            return os.path.join(path, name)
        path = os.path.dirname(path)
    return None


def list_opened_files():
    """
    return a list of opened REAL files(excluding buftype of nofile etc).
    """
    return [b.name for b in vim.buffers
            if not len(b.options['buftype']) and os.path.isfile(b.name)]
