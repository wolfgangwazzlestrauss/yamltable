# CLI

Utility for working with YAML files organized similar to a relational database
table.

**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `--install-completion`: Install completion for the current shell.
- `--show-completion`: Show completion for the current shell, to copy it or
  customize the installation.
- `--help`: Show this message and exit.

**Commands**:

- `index`: Get row at INDEX in FILE_PATH.
- `list`: List all dictionary KEY values in FILE_PATH.
- `search`: Search dictionaries in FILE_PATH with...
- `sort`: Sort dictionaries in FILE_PATH by KEY values.
- `validate`: Check that every dictionary in FILE_PATH has...

## `index`

Get row at INDEX in FILE_PATH.

**Usage**:

```console
$ index [OPTIONS] INDEX FILE_PATH
```

**Options**:

- `--help`: Show this message and exit.

## `list`

List all dictionary KEY values in FILE_PATH.

**Usage**:

```console
$ list [OPTIONS] KEY FILE_PATH
```

**Options**:

- `--help`: Show this message and exit.

## `search`

Search dictionaries in FILE_PATH with matching KEY and VALUE pairs.

**Usage**:

```console
$ search [OPTIONS] KEY VALUE FILE_PATH
```

**Options**:

- `--help`: Show this message and exit.

## `sort`

Sort dictionaries in FILE_PATH by KEY values.

**Usage**:

```console
$ sort [OPTIONS] KEY FILE_PATH
```

**Options**:

- `--help`: Show this message and exit.

## `validate`

Check that every dictionary in FILE_PATH has conforms to its schema.

**Usage**:

```console
$ validate [OPTIONS] FILE_PATH
```

**Options**:

- `--help`: Show this message and exit.
