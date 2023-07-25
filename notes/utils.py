import redis
import json


class RedisNote:
    redis = redis.Redis(host='localhost', port=6379, decode_responses=True)

    @classmethod
    def save(cls, user_id, note_data):
        cls.redis.hset(f'user_{user_id}', f'note_{note_data.get("id")}', json.dumps(note_data))

    @classmethod
    def retrive(cls, user_id):
        note = cls.redis.hgetall(f'user_{user_id}').values()
        if not note:
            return None
        return [json.loads(i) for i in note]

    @classmethod
    def delete(cls, user_id, note_id):
        cls.redis.hdel(f'user_{user_id}', f'note_{note_id}')
