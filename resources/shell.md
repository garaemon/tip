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
