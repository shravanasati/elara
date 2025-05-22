# `elara`

elara is a CLI tool to convert Jupyter notebooks into *pretty* HTML documents.

elara is very much customizable while providing sane defaults.

For more information, visit https://github.com/shravanasati/elara

**Usage**:

```console
$ elara [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `list-themes`: Lists all built-in themes.
* `convert`: Converts multiple jupyter notebooks into...

## `elara list-themes`

Lists all built-in themes.

**Usage**:

```console
$ elara list-themes [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `elara convert`

Converts multiple jupyter notebooks into HTML documents. Any options passed, will be applied to all
the jupyter notebooks.

Font options can be prefixed with `gf:` to use Google Fonts directly.

**Usage**:

```console
$ elara convert [OPTIONS] FILES...
```

**Arguments**:

* `FILES...`: [required]

**Options**:

* `--theme TEXT`: The theme for code blocks.  [default: vs]
* `--font TEXT`: Font for overall document.  [default: sans-serif]
* `--code-font TEXT`: Font for code and output.  [default: monospace]
* `--help`: Show this message and exit.
