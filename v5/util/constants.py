from typing import ClassVar, Final

__all__ = (
    'DiscordInvites',
    'Resources'
)


class DiscordInvites:
    """
    Constant value of some invite urls
    """
    discord_base_invite: Final[str] = "https://discord.gg/"
    official_community_code: Final[str] = "taVq6rw"
    bug_report_code: Final[str] = "aC4wngr"
    
    @property
    def officialCommunity(self) -> str:
        return self.discord_base_invite + self.official_community_code

    @property
    def bugReport(self) -> str:
        return self.discord_base_invite + self.official_community_code


class Resources:
    """
    Some resource paths
    """
    class Latte:
        Latte2020: str = 'profile/Latte2020_re2.png'
        LatteChar: str = 'profile/Latte2020_char_noarm.png'
        LatteMerong: str = 'profile/Latte_merong_copyright_BIG.png'
        Latte2019: str = 'profile/profile_by_RED_PIXEL_BLOCK_bigger_w_Copyright.png'
        Thanos: str = 'thanos_latte.png'
