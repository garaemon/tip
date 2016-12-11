## Find files which have specific suffix

```
find . -name "*.md"
```

## Replace specific keyword under some directories

```
find . -type f -print0 | xargs -0 sed -i -e 's/foo/bar/g'
```

## Exclude specifi directory with find command

```
find . -type d -name foo -prune -o [condition]
find . -type d -name foo -prune -o -name '*.md' -print
```

## Get current directory of shell script in bash

```sh
cwd=$(dirname "${0}")
expr "${0}" : "/.*" > /dev/null || cwd=$(cd "${cwd}" && pwd)
```

## Redirect all the output from command

```sh
command >/dev/null 2>&1
```

## Record and playback terminal work

Use ttyrec and [seq2gif](https://github.com/saitoha/seq2gif).

Record
```
ttyrec /path/to/log/file
```

Convert to gif animation. Do not forget to specify columns.
```
seq2gif -w $COLUMNS < /path/to/log/file > /path/to/gif
```
