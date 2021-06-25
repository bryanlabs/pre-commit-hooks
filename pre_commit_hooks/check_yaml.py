import argparse
from typing import Any
from typing import Generator
from typing import NamedTuple
from typing import Optional
from typing import Sequence

import ruamel.yaml

class Ref:
    yaml_tag = u'!Ref:'

    def __init__(self, value, style=None):
        self.value = value
        self.style = style

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_scalar(cls.yaml_tag,
                                            u'{.value}'.format(node), node.style)

    @classmethod
    def from_yaml(cls, constructor, node):
        return cls(node.value, node.style)

    def __iadd__(self, v):
        self.value += str(v)
        return self
class Sub:
    yaml_tag = u'!Sub:'

    def __init__(self, value, style=None):
        self.value = value
        self.style = style

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_scalar(cls.yaml_tag,
                                            u'{.value}'.format(node), node.style)

    @classmethod
    def from_yaml(cls, constructor, node):
        return cls(node.value, node.style)

    def __iadd__(self, v):
        self.value += str(v)
        return self
class GetAtt:
    yaml_tag = u'!GetAtt:'

    def __init__(self, value, style=None):
        self.value = value
        self.style = style

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_scalar(cls.yaml_tag,
                                            u'{.value}'.format(node), node.style)

    @classmethod
    def from_yaml(cls, constructor, node):
        return cls(node.value, node.style)

    def __iadd__(self, v):
        self.value += str(v)
        return self
class Join:
    yaml_tag = u'!Join:'

    def __init__(self, value, style=None):
        self.value = value
        self.style = style

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_scalar(cls.yaml_tag,
                                            u'{.value}'.format(node), node.style)

    @classmethod
    def from_yaml(cls, constructor, node):
        return cls(node.value, node.style)

    def __iadd__(self, v):
        self.value += str(v)
        return self

yaml = ruamel.yaml.YAML(typ='rt')
yaml.register_class(Ref)
yaml.register_class(Sub)
yaml.register_class(GetAtt)
yaml.register_class(Join)


def _exhaust(gen: Generator[str, None, None]) -> None:
    for _ in gen:
        pass


def _parse_unsafe(*args: Any, **kwargs: Any) -> None:
    _exhaust(yaml.parse(*args, **kwargs))


def _load_all(*args: Any, **kwargs: Any) -> None:
    _exhaust(yaml.load_all(*args, **kwargs))


class Key(NamedTuple):
    multi: bool
    unsafe: bool


LOAD_FNS = {
    Key(multi=False, unsafe=False): yaml.load,
    Key(multi=False, unsafe=True): _parse_unsafe,
    Key(multi=True, unsafe=False): _load_all,
    Key(multi=True, unsafe=True): _parse_unsafe,
}


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m', '--multi', '--allow-multiple-documents', action='store_true',
    )
    parser.add_argument(
        '--unsafe', action='store_true',
        help=(
            'Instead of loading the files, simply parse them for syntax.  '
            'A syntax-only check enables extensions and unsafe contstructs '
            'which would otherwise be forbidden.  Using this option removes '
            'all guarantees of portability to other yaml implementations.  '
            'Implies --allow-multiple-documents'
        ),
    )
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    load_fn = LOAD_FNS[Key(multi=args.multi, unsafe=args.unsafe)]

    retval = 0
    for filename in args.filenames:
        try:
            with open(filename, encoding='UTF-8') as f:
                load_fn(f)
        except ruamel.yaml.YAMLError as exc:
            print(exc)
            retval = 1
    return retval


if __name__ == '__main__':
    exit(main())
