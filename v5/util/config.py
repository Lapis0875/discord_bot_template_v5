from __future__ import annotations
import asyncio
import json
import os
from functools import reduce
from typing import NoReturn, ClassVar, Final, Optional, Any, List, Dict
from .resources import JsonFile
from .type_hints import JSON
from .abstracts import JsonObject
from .logging_util import getLogger, LogLevels


__all__ = (
    'Config',
)

logger = getLogger('utils.config', LogLevels.DEBUG)

__instance_storage__: Dict[str, Config] = {}


class Config(JsonObject):
    """Configuration storage & manager"""

    root: Final[ClassVar[str]] = 'config'

    @classmethod
    def fromJson(cls, name: str, content: JSON) -> Config:
        return cls(name=name, content=content)

    def toJson(self) -> JSON:
        return self._content

    @property
    def raw(self) -> JSON:
        return self._content

    def __call__(self, *args, **kwargs):
        try:
            name: str = kwargs['name']
        except KeyError:
            name: str = tuple(filter(lambda arg: isinstance(arg, str), args))[0]
        instance = __instance_storage__.get(name)
        if instance is not None:
            return instance
        else:
            return super().__call__(*args, **kwargs)

    def __init__(self, name: str, content: Optional[JSON] = None):
        self._name = name
        self._file: JsonFile = JsonFile(path=os.path.join(self.root, f'{name}.json'), content=content)
        self._content: JSON = self.__internal__read()
        logger.debug(f'JsonFile {self._file} attached to config {name}')
        contentLoad: asyncio.Task = asyncio.get_event_loop().create_task(self.load(), name=f'Config[name={name}].load')
        contentLoad.add_done_callback(self.__setAvailable)
        logger.debug(
            f'Scheduling content load coro in event loop. current task : {contentLoad}'
        )
        __instance_storage__[name] = self

    @property
    def file(self) -> JsonFile:
        return self._file

    async def load(self) -> NoReturn:
        self._content = await self._file.read()
        logger.debug(f'result of config load : {self._content}')

    def isLoaded(self) -> bool:
        return bool(self._content)

    def __internal__read(self) -> JSON:
        with open(file=self._file._relPath, mode='rt', encoding='utf-8') as f:
            text = f.read()
        return json.loads(text)

    def __setAvailable(self, result):
        logger.debug(result)
        logger.debug(f'Config file {self._name} finished loading and is now available!')

    async def save(self) -> NoReturn:
        await self._file.write(self._content)

    def get(self, key: str) -> Optional[Any]:
        """Retrieve item in config using eval [EXPERIMENT]
        Usage:
            Config.get(key1.key2.key3) == Config.raw[key1][key2][key3]
        Args:
            key (str):
                'key1.key2.key3' style dictionary keys. This will be split using '.', and used to get content.
        :return:
        """

        logger.debug(f'{self!r}.get - key : {key}')
        try:
            res = eval(r'self._content' + ''.join(f"['{k}']" for k in key.split('.') if k))
            logger.debug(f'get2 : {res}')
            return res
        except (KeyError, AttributeError):
            # None.get(key) -> AttributeError
            # In case of this, return None.
            logger.debug(f'{self!r}.get - Cannot find corresponding data in config. Return None.')
            return None

    def __repr__(self):
        return f'Config<{self._name}>'



