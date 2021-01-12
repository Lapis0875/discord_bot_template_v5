from typing import Union, List

import aiohttp
import nacl
from discord.ext import commands
from v5.core import Latte
from v5.ext.cogs import LatteCog
from v5.models.discordAPI import ApplicationCommand, InteractionResponseType


class DiscordPreviewCog(LatteCog):
    """Cog for V5 API test features (not released, or not implemented in dpy."""
    
    def __init__(self, bot: Latte):
        super(DiscordPreviewCog, self).__init__(bot)
        self._application_commands: List[ApplicationCommand]

        self._publicKey = nacl

    @listener
    async def on_socket_raw_receive(self, msg: Union[bytes, str]):
        print(f'[DiscordPreviewCog] [socket_raw_receive] msg : {msg}')
        if msg["t"] != "INTERACTION_CREATE":
            return
        to_use = msg["d"]
        print(to_use["data"]["name"])
        if to_use["data"]["name"] == "test": # 커맨드 이름
            req_url = f"https://discord.com/api/v8/interactions/{to_use['id']}/{to_use['token']}/callback"
            _resp = {
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE.value,
                "data": {
                    "tts": False,
                    "content": "대충 테스트",
                    "embeds": [],
                    "allowed_mentions": []
                }
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(req_url, json=_resp) as resp:
                    print(resp.status)
                    print(await resp.text())

    @commands.command(
        name='secretMessage',
        description=''
    )
    async def cmdSecretMessage(self, ctx: commands.Context):
        """Sends secret message like Clyde does.
        This can be done by setting Message Flag to 1 << 6

        :param ctx:
        :return:
        """
        msg = await ctx.send('Lorem ipsum from Latte`s secret message!')
        await msg.edit(flags=1 << 6)


def setup(bot: Latte):
    """Function called when extension is loaded."""
    bot.logger.debug(
        'Registering extension "discordPreview"'
    )
    bot.add_cog(DiscordPreviewCog(bot))


def teardown(bot: Latte):
    """Function called when extension is unloaded."""
    bot.logger.debug(
        'Removing extension "discordPreview"'
    )
    bot.remove_cog(bot.get_cog('DiscordPreview'))
