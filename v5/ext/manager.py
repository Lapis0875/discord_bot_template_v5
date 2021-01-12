from discord.ext.commands import AutoShardedBot


class ExtensionManager:
    def __init__(self, bot: AutoShardedBot, config):
        self._config = config
        self._bot: AutoShardedBot = bot

    def load(self, name: str):
        self._bot.load_extension(name)

    def unload(self, name: str):
        self._bot.unload_extension(name)

    def reload(self, name: str):
        self._bot.reload_extension(name)
