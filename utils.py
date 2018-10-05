def get_input(*args):
  '''works the same in python 2 and 3'''
  return raw_input(*args) if 'raw_input' in dir(vars()['__builtins__']) else input(*args)

def print_out(*args):
  '''works the same in python 2 and 3'''
  print(' '.join(map(str, args)))

def maybeFloat(string):
  '''Converts NaN values to None.
  While NaN is a valid floating point value,
  it is truthy and cannot be tested for equality'''
  return None if string == "NaN" else float(string)

#https://www.rexegg.com/regex-disambiguation.html#noncap
def get_arg(name, argv, numeric=True, has_val=False):
  if has_val:
    arg_format = "(?:--"+ name+"|"+"-"+name[0]+")"
    value_format = r"(\d+)(?:\s|$)" if numeric else r"(?:\"(.+)\")|(.+(?:\s|$))"
    groups = re.search(arg_format+"\s"+value_format, ' '.join(argv))
    return None if not groups else groups.group(1)
  else:
    return '--'+name in argv or '-'+name in argv

class SubDirectory():
  '''this class allows you to use the with-statement when working in subdirectories'''
  def __init__(self, dir_name):
    self.dir_name = dir_name
  def __enter__(self):
    try:
      mkdir(self.dir_name)
    except:  # os specific error if directory exists already
      chdir(self.dir_name)
  def __exit__(self, *_):
    chdir('..')

def celsius_to_farenheit(x):
  return (x+32)*9/5
