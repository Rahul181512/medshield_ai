from collections import defaultdict

from app.services.redis_service import redis_service


class PlaceholderMapper:
    """
    Generates consistent placeholders and stores
    mappings in Redis.
    """

    def __init__(
        self,
        session_id: str,
        ttl: int = 3600,
    ):
        self.session_id = session_id
        self.ttl = ttl

        self.counters = defaultdict(int)

    def _forward_key(
        self,
        entity_type: str,
        value: str,
    ) -> str:
        return (
            f"medshield:{self.session_id}:"
            f"forward:{entity_type}:{value.lower()}"
        )

    def _reverse_key(
        self,
        placeholder: str,
    ) -> str:
        return (
            f"medshield:{self.session_id}:"
            f"reverse:{placeholder}"
        )

    def _counter_key(
        self,
        entity_type: str,
    ) -> str:
        return (
            f"medshield:{self.session_id}:"
            f"counter:{entity_type}"
        )

    def get_placeholder(
        self,
        entity_type: str,
        value: str,
    ) -> str:
        """
        Return the same placeholder for repeated values.
        """

        forward_key = self._forward_key(
            entity_type,
            value,
        )

        existing = redis_service.get(
            forward_key
        )

        if existing:
            return existing

        counter_key = self._counter_key(
            entity_type
        )

        current = redis_service.get(
            counter_key
        )

        counter = int(current) if current else 0
        counter += 1

        placeholder = (
            f"[{entity_type}_{counter:03d}]"
        )

        redis_service.set(
            forward_key,
            placeholder,
            self.ttl,
        )

        redis_service.set(
            self._reverse_key(placeholder),
            value,
            self.ttl,
        )

        redis_service.set(
            counter_key,
            str(counter),
            self.ttl,
        )

        return placeholder

    def get_original_value(
        self,
        placeholder: str,
    ):
        """
        Return original value from Redis.
        """

        return redis_service.get(
            self._reverse_key(placeholder)
        )

    def get_all_mappings(self):
        """
        Return all placeholder-to-original-value
        mappings for the current session.
        """

        pattern = (
            f"medshield:{self.session_id}:"
            f"reverse:*"
        )

        redis_mappings = (
            redis_service.get_by_pattern(
                pattern
            )
        )

        mappings = {}

        prefix = (
            f"medshield:{self.session_id}:"
            f"reverse:"
        )

        for key, value in redis_mappings.items():

            placeholder = key[len(prefix):]

            mappings[placeholder] = value

        return mappings

    def clear_session(self):
        """
        Clear all mappings for the current session.

        Session cleanup will be implemented
        after integration testing.
        """
        pass