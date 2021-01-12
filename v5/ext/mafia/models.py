from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, NoReturn

import discord
from chronous.events import BaseEvent, DefaultBus


class MafiaEvent(BaseEvent):
    def __init__(self, loopable: bool):
        super(MafiaEvent, self).__init__(loopable)

    def __repr__(self) -> str:
        return f'<MafiaEvent(name={self._name})>'

"""
Game Events
"""

class MafiaGameEvent(MafiaEvent):
    def __init__(self):
        super(MafiaGameEvent, self).__init__(loopable=True)

    def __repr__(self) -> str:
        return f'<MafiaGameEvent(name={self._name})>'


class VoteStartEvent(MafiaGameEvent):
    vote_channel: discord.TextChannel = None

    def __init__(self):
        super(VoteStartEvent, self).__init__()

    def __repr__(self) -> str:
        return f'<MafiaGameEvent.VoteStart(name={self._name})>'


class VoteFinishEvent(MafiaGameEvent):
    def __init__(self):
        super(VoteFinishEvent, self).__init__()

    def __repr__(self) -> str:
        return f'<MafiaGameEvent.VoteFinish(name={self._name})>'


"""
User Events
"""


class MafiaUserEvent(MafiaEvent):
    def __init__(self):
        super(MafiaUserEvent, self).__init__(loopable=False)

    def __repr__(self) -> str:
        return f'<MafiaUserEvent(name={self._name})>'


# May be non-necessary
@DeprecationWarning
class UserVoteEvent(MafiaUserEvent):
    def __init__(self, user: User, target: User, count: int = 1):
        super(UserVoteEvent, self).__init__()
        self.user: User = user        # 투표를 한 유저
        self.target: User = target    # 투표를 받은 유저
        self.count: int = count      # 추가할 투표 수 (일반적으로는 1이지만, 정치인은 2)

    def __repr__(self) -> str:
        return f'<MafiaUserEvent.UserVote(name={self._name})>'


class KillEvent(MafiaUserEvent):
    def __init__(self, user: User, target: User):
        super(KillEvent, self).__init__()
        self.user: User = user      # 타겟을 죽인 유저
        self.target: User = target  # 죽은 유저

    def __repr__(self) -> str:
        return f'<MafiaUserEvent.Kill(user={self.user},target={self.target})>'


class MafiaGameManager:
    games: Dict[int, MafiaGame] = []            # All games
    waiting_games: Dict[int, MafiaGame] = []    # Games Waiting for start
    running_games: Dict[int, MafiaGame] = []    # Games started
    joined_users: List[User] = []               # Users joined in game

    @classmethod
    def registerGame(cls, game: MafiaGame):
        cls.running_games[game.id] = game

    @classmethod
    def _getGame(cls, games: Dict[int, MafiaGame], game_id: int) -> Optional[MafiaGame]:
        try:
            return games[game_id]
        except KeyError:
            return None

    @classmethod
    def findGame(cls, game_id: int) -> Optional[MafiaGame]:
        return cls._getGame(cls.games, game_id)

    @classmethod
    def findWaitingGame(cls, game_id: int) -> Optional[MafiaGame]:
        return cls._getGame(cls.waiting_games, game_id)

    @classmethod
    def findRunningGame(cls, game_id: int) -> Optional[MafiaGame]:
        return cls._getGame(cls.running_games, game_id)


class Game(ABC):
    """Abstract Base Class of Game instance."""
    @property
    @abstractmethod
    def id(self) -> int:    ...
    @property
    @abstractmethod
    def name(self) -> str:  ...
    @property
    @abstractmethod
    def isWaiting(self) -> bool:    ...
    @property
    @abstractmethod
    def isRunning(self) -> bool:    ...
    @abstractmethod
    def joinUser(self, user: discord.User) -> User: ...
    @abstractmethod
    def leaveUser(self, user_id: int) -> User:  ...
    @abstractmethod
    async def start(self) -> NoReturn:    ...
    @abstractmethod
    async def stop(self) -> int:  ...


class MafiaGame(Game):
    """MafiaGame object which implements 'Game' ABC."""
    def __init__(self, game_id: int, name: str):
        """
        Args:
            game_id (int): integer value of id of the game.
            name (str): string value of the game name.
        """
        self._id: int = game_id
        self._name: str = name
        self._users: Dict[int, User] = {}
        self._isWaiting: bool = True
        self._isRunning: bool = False

    @property
    def id(self) -> int:
        """id of the MafiaGame object. Each MafiaGame object has unique id."""
        return self._id

    @property
    def name(self) -> str:
        """name of the MafiaGame object. Can be duplicated through games."""
        return self._name

    @property
    def isWaiting(self) -> bool:
        """Flag value which indicates whether the game is waiting for users or not."""
        return self._isWaiting

    @property
    def isRunning(self) -> bool:
        """Flag value which indicates whether the game is running or not."""
        return self._isRunning

    def joinUser(self, user: discord.User) -> User:
        user = User(game_id=self._id, user=user)
        self._users[user.id] = user
        return user

    def leaveUser(self, user_id: int) -> User:
        return self._users.pop(user_id)

    async def start(self) -> NoReturn:
        while False:
            pass
        await self.stop()

    async def stop(self) -> int:
        pass


class MafiaGameException(Exception):
    """Exception occured during Mafia Game"""
    def __init__(self, game_id: Optional[int]):
        self.game_id: Optional[int] = game_id

    def __repr__(self) -> str:
        return f'<MafiaGameException(game_id={self.game_id})>'

    def __str__(self) -> str:
        return f'An exception occured during Mafia Game with id {self.game_id}.'


class MafiaGameNotFound(MafiaGameException):
    """Exception occured when retrieving mafia game instance failed"""
    def __init__(self, game_id: Optional[int]):
        super(MafiaGameNotFound, self).__init__(game_id)

    def __repr__(self) -> str:
        return f'<MafiaGameException(game_id={self.game_id}).NotFound>'

    def __str__(self) -> str:
        return f'Mafia game instance with id {self.game_id} not found!'


class GameObject:
    def __init__(self, id: int, game_id: int):
        self._id = id
        setattr(self, '__game_id__', game_id)

    @property
    def id(self) -> int:
        return self._id


class User(GameObject):
    def __init__(self, game_id: int, user: discord.User):
        super(User, self).__init__(user.id, game_id)
        self._user: discord.User = user
        self._name: str = user.display_name
        self._avatar_url: str = user.avatar_url
        self._dm_id: int = user.dm_channel.id

    @property
    def name(self) -> str:
        return self._name

    @property
    def profile(self) -> str:
        return self._avatar_url

    async def vote(self, channel: discord.TextChannel):
        game_id: int = getattr(self, '__game_id__', None)
        game: MafiaGame = MafiaGameManager.findRunningGame(game_id)
        if game is None:
            raise MafiaGameNotFound(game_id)
        else:
            await game.getVoteEmbed()


    @DefaultBus.listen
    async def onVoteStart(self, e: VoteStartEvent):
        await self.vote(e.vote_channel)

