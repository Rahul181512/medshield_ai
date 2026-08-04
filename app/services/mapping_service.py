from collections import defaultdict


class PlaceholderMapper:
    """
    Generates consistent placeholders for detected entities.
    """

    def __init__(self):

        self.mapping = {}
        self.counters = defaultdict(int)

    def get_placeholder(self, entity_type: str, value: str) -> str:
        """
        Return the same placeholder for repeated values.
        """

        key = (
            entity_type,
            value.lower(),
        )

        if key in self.mapping:
            return self.mapping[key]

        self.counters[entity_type] += 1

        placeholder = (
            f"[{entity_type}_{self.counters[entity_type]:03d}]"
        )

        self.mapping[key] = placeholder

        return placeholder