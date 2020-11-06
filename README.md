# YamlTable

![](https://img.shields.io/pypi/v/yamltable)
![](https://img.shields.io/pypi/pyversions/yamltable.svg)
![](https://github.com/wolfgangwazzlestrauss/yamltable/workflows/build/badge.svg)
![](https://codecov.io/gh/wolfgangwazzlestrauss/yamltable/branch/master/graph/badge.svg)
![](https://img.shields.io/badge/code%20style-black-000000.svg)
![](https://img.shields.io/github/repo-size/wolfgangwazzlestrauss/yamltable)
![](https://img.shields.io/github/license/wolfgangwazzlestrauss/yamltable)

---

**Documentation**: https://wolfgangwazzlestrauss.github.io/yamltable

**Source Code**: https://github.com/wolfgangwazzlestrauss/yamltable

---

YamlTable is a Python command line utility for working with YAML files organized
similar to a relational database table. It supports YAML files organized as a
list of dictionaries, which share key names and value types. YamlTable provides
commands for listing, searching, sorting, etc. data from the supported files.

## Supported YAML File Organizations

YamlTable works with YAML files organized as a list of dictionaries with similar
key names and value types.

```yaml
- name: awscli
  description: Amazon Web Services command line client
  website: https://aws.amazon.com/
- name: glances
  description: operating system monitoring interface
  website: https://github.com/nicolargo/glances
```

The JSON schema support is included for YAML files organized as:

```yaml
schema:
  $schema: http://json-schema.org/draft-07/schema#
  description: pipx package metadata schema
  type: object
  properties:
    name:
      type: string
      pattern: "^[\\w-]+$"
    description:
      type: string
    website:
      type: string
  required:
    - name
    - description
    - website
  additionalProperties: false
rows:
  - name: awscli
    description: Amazon Web Services command line client
    website: https://aws.amazon.com/
  - name: glances
    description: operating system monitoring interface
    website: https://github.com/nicolargo/glances
```

## Getting Started

### Installation

YamlTable can be installed for Python 3.6+ with

```console
pip install yamltable
```

For more installation instructions, see the
[Install](https://wolfgangwazzlestrauss.github.io/yamltable/install/) section of
the documentation.

### Commands

YamlTable provides a CLI command
[reference](https://wolfgangwazzlestrauss.github.io/yamltable/api/cli/) in its
documenation.

## Contributing

For guidance on setting up a development environment and how to make a
contribution, see the
[Contributing](https://wolfgangwazzlestrauss.github.io/yamltable/contrib/)
section of the documentation.

## License

YamlTable is licensed under the
[MIT license](https://wolfgangwazzlestrauss.github.io/yamltable/license/).
