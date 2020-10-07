# Install

## Installing Python

YamlTable requires Python 3.6+ as a dependency. You can download Python from
their [official site](https://www.python.org/downloads/). If you need to manage
multiple Python versions, [pyenv](https://github.com/pyenv/pyenv) is recommended
for Linux or macOs, and [pyenv-win](https://github.com/pyenv-win/pyenv-win) is
recommended for Windows.

## Installing YamlTable

YamlTable can be installed with the PIP package manager.

```console
pip install --user yamltable
```

If you receive a script warning about the install location not being found on
your `PATH`, then add the install location to your `PATH` environment variable.

## Diving In

Once YamlTable is installed, you can try it out from the command line with
`yamltable --help` or import it in a Python script with `import yamltable`. For
instructions about using YamlTable from the command line, visit the
[CLI guide](/api/cli.md). For instructions about using YamlTable as a Python
library, visit the [API reference](/api/index.md).
