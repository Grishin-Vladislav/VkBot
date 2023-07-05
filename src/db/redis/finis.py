import redis


class FiniteStateMachine:
    def __init__(self, connection: redis.Redis) -> None:
        self.__redis = connection

    def get(self, user_id: int) -> str | None:
        state = self.__redis.hget(f'{user_id}:states', 'current')
        return state

    def set(self, user_id: int, state: str) -> None:
        self.__redis.hset(f'{user_id}:states', 'current', state)
        return
