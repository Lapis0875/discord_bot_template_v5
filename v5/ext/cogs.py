from discord.ext.commands import Cog
from v5.core import Latte
import os


class LatteCog(Cog):
    """
    Base Cog class fot Latte`s extension feature.
    """

    locals().update({"listener": Cog.listener})

    def __init__(self, bot: Latte) -> None:
        """Initialize Cog.
        Args:
            bot (class: Latte): discord.py Bot instance, especially Latte instance.
        """
        self._bot = bot
        print(os.getcwd())
        print(__file__)
        print(os.path.relpath(os.getcwd(), __file__))

        self.log_prefix = os.path.relpath(os.getcwd(), __file__)   # LatteExt.py -> "LatteExt" -> [LatteExt] [info] ...
        bot.logger.info(
            msg=f"[{self.log_prefix}] Injecting key from ext_map matching with module path into cog ..."
                "(To access to cog instance in easier way.)"
        )
        # Set __cog_name__ value as extension name registered in extension map.
        self.__cog_name__ = self.__class__.__name__.strip('Cog')
        self.category = bot.ext.find_category(self.__cog_name__)
        bot.logger.info(
            msg=f"[{self.log_prefix}] {self.category}.{self.__cog_name__} loaded!"
        )

    @property
    def bot(self) -> Latte:
        return self._bot
