import asyncio
import json
import os
from enum import Enum
from typing import Union, Dict, NoReturn, Literal, Optional
import aiofile

from .logging_util import getLogger, Logger, LogLevels
from .type_hints import JSON

__all__ = (
    'ResourceType',
    'ResourceFile',
    'JsonFile'
)


logger = getLogger(name='utils.resources', level=LogLevels.DEBUG)


class ResourceType(Enum):
    BYTES = 'b'
    TEXT = 't'


class ResourceFile:
    """Object holding resource data."""
    def __init__(
            self,
            path: str,
            resType: ResourceType,
            encoding: str = 'utf-8',
            content: Optional[Union[str, bytes]] = None
    ):
        """Initialize ResourceHolder object.

        Args:
            path: Path to the resource. Must contain filename and extension name (./path/to/file.txt)
            resType: ResourceType Enum value which indicates the file must be managed as bytes or text.
        """
        self._relPath: str = path
        print(path)
        self._resType: ResourceType = resType
        if resType == resType.TEXT:
            self._encoding = encoding
        print(self.exists())
        if not self.exists():
            asyncio.get_event_loop().create_task(self.create())

        if content is not None:
            asyncio.get_event_loop().create_task(self.write(content))

    @property
    def relativePath(self) -> str:
        return self._relPath

    @property
    def resourceType(self) -> str:
        return self._resType.value

    def exists(self) -> bool:
        return os.path.exists(self._relPath)

    async def create(self, content: Optional[Union[str, bytes]] = None) -> bool:
        if content is None:
            if self._resType == ResourceType.TEXT:
                content = ''
            elif self._resType == ResourceType.BYTES:
                content = bytes()

        await self.write(content)

    def open(
            self,
            mode: str = Literal['r', 'w', 'a', 'r+', 'w+']
    ) -> Union[aiofile.BinaryFileWrapper, aiofile.TextFileWrapper]:
        params: Dict[str, str] = {
            'file_name': self._relPath,
            'mode': f'{mode}{self._resType.value}'
        }
        if self._resType == ResourceType.TEXT:
            params['encoding'] = self._encoding
        return aiofile.async_open(**params)

    async def read(self) -> Union[bytes, str]:
        async with self.open('r') as f:
            return await f.read()

    async def readLine(self) -> str:
        async with self.open('r') as f:
            return await f.readLine()

    async def write(self, content: Union[bytes, str]) -> NoReturn:
        if self._resType == ResourceType.TEXT and not isinstance(content, str):
            raise TypeError('Text file is only able to write string contents in order to prevent file problems.')
        elif self._resType == ResourceType.BYTES and not isinstance(content, bytes):
            raise TypeError('Bytes file is only able to write bytes contents in order to prevent file problems.')
        async with self.open('w') as f:
            await f.write(content)


class JsonFile(ResourceFile):
    """ResourceHolder specialized to manage configurations."""
    def __init__(self, path: str, content: Optional[JSON]):
        super(JsonFile, self).__init__(path, ResourceType.TEXT)

        if content is not None:
            asyncio.create_task(self.write(content))

    async def read(self) -> JSON:
        text: str = await super(JsonFile, self).read()
        return json.loads(text)

    async def write(self, content: JSON) -> NoReturn:
        text: str = json.dumps(obj=content, indent=4, ensure_ascii=False)
        await super(JsonFile, self).write(text)
