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

## Colorize logging by coloredlogs

```python
import logging
import coloredlogs
coloredlogs.install(level=logging.DEBUG)

logging.error("This is error")
```

## Specifying logging format in coloredlogs

```python
import logging
import coloredlogs

coloredlogs.install(fmt='%(asctime)s [%(levelname)s] %(message)s')

logging.error("This is error")
```

## Color style in coloredlogs

Use `coloredlogs.DEFAULT_FIELD_STYLES` and `field_style` keyword of
`coloredlogs.install`.

```python
import logging
import coloredlogs

field_styles = coloredlogs.DEFAULT_FIELD_STYLES
field_styles['levelname'] = {'color': 'white', 'bold': True}
coloredlogs.install(field_styles=field_styles)

logging.error("This is error")

```
