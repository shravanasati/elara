# elara 🌙

elara is a CLI tool to convert Jupyter notebooks into *pretty* HTML documents.

Named after one of Jupiter's moons, elara's motive is to render beautiful HTML markups, with support for a number of themes. It has multiple built-in themes, and supports VSCode themes out of the box. 

elara aims to support only nbformat v4 (you are most likely already using it).


### Installation

elara is available on [PyPI](https://pypi.org/project/elarapy).

**recommended way** to install (isolated dependencies):
```
pipx install elarapy
```

**using pip** on linux/mac:
```
pip3 install elarapy
```

**using pip** on windows:
```
pip install elarapy
```



### **Usage**:

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

**Examples**:

* Using a built in theme with pre-installed fonts:
	```console
	elara convert ./file.ipynb --theme "nord" --font "Arial" --code-font "Consolas"
	```

* Using Google fonts
	```console
	elara convert ./file.ipynb --theme "gruvbox" --font "gf:Geist" --code-font "gf:Geist Mono"
	```

* Using a VSCode theme
	```console
	elara convert ./file.ipynb --theme path/to/theme.json 
	```