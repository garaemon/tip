## Check python code syntax by flake8

```
flake8 foo.py
flake8 .
```

## Ignore multiple files from flake8 in `tox.ini`.

Do not use spaces between commas.
```
[flake8]
exclude = foo.py,bar.py.piyo.py
```

## Search regular expression and know its position

Use `start` and `end` method.

```python
import re
for m in re.compile('a').finditer('hoge a fuga a piyo'):
  print (m.start(), m.end())
```

## Ignore case (case-insentive) regular expression search using re

```python
regexp = re.compile(regexp_str, re.IGNORE)
```

## Implement multiple AND search using regular expression with ignoring order

```python
re.compile('^(?=.*foo)(?=.*bar)').search('abc foo abc bar')
```
