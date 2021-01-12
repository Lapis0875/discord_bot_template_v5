from __future__ import annotations

import aiohttp
import inspect
from typing import Optional, List, NamedTuple
from discord import VersionInfo
from discord.ext.commands import Bot

from v5.ext.manager import ExtensionManager
from v5.models.discordAPI import *
from v5.models.slash import *
from v5.util.type_hints import JSON
from v5.util.config import Config
from v5.util.logging_util import getLogger, Logger, LogLevels


class Info(NamedTuple):
    name: str
    version: VersionInfo


class V5(Bot):
    """
    V5 core of discord Bot
    """

    # Bot Info
    @property
    def libInfo(self) -> Info:
        return self._libInfo

    def __init__(self):
        self.config: Config = Config(name='bot')
        self._ext: ExtensionManager = ExtensionManager(bot=self, config=self.config.get('ext'))
        self._logger: Logger = getLogger('core.Latte', LogLevels.DEBUG)
        self._libInfo = Info(
            name='V5Engine',
            version=VersionInfo(
                major=0,
                minor=1,
                micro=0,
                releaselevel='dev',
                serial=0
            )
        )

        # Application Commands
        
        super().__init__(
            command_prefix=self.config.get('prefix'),
            help_command=None,
            description="카페라테를 좋아하는 개발자가 만든 디스코드 봇이에요!"
        )

    @property
    def logger(self) -> Logger:
        return self._logger

    def debug(self, *args, **kwargs):
        return self._logger.debug(*args, **kwargs)

    def run(self, *args, **kwargs):
        super().run(self.config.get('token'), *args, **kwargs)

    # HTTP request util
    def getAuthHeader(self) -> JSON:
        return {
            'Authorization': f'Bot {self.config.get("token")}'
        }

    # Application Command features
    async def createGlobalCommand(
            self,
            name: str,
            description: str,
            options: Optional[List[JSON]] = None
    ) -> ApplicationCommand:
        commandJson: JSON = {
            'name': name,
            'description': description
        }
        if isinstance(options, list):
            commandJson['options'] = [option for option in options if isinstance(option, dict)]

        async with aiohttp.ClientSession() as s:
            res = await s.post(
                json=commandJson
            )
            command = ApplicationCommand(await res.json())
            self.__application_commands__.append(command)
            return command

    async def createGuildCommand(
            self,
            guild_id: int,
            name: str,
            description: str,
            options: Optional[List[JSON]] = None
    ) -> ApplicationCommand:
        commandJson: JSON = {
            'name': name,
            'description': description
        }
        if isinstance(options, list):
            commandJson['options'] = [option for option in options if isinstance(option, dict)]

        async with aiohttp.ClientSession() as s:
            res = await s.post(
                url='',
                json=commandJson
            )
            command = ApplicationCommand(await res.json())
            self.__application_commands__.append(command)
            return command