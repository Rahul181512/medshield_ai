from collections import defaultdict


class PlaceholderMapper:
    """
    Generates consistent placeholders and maintains
    forward and reverse mappings.
    """

    def __init__(self):

        # (ENTITY_TYPE, VALUE) -> PLACEHOLDER
        self.forward_mapping = {}

        # PLACEHOLDER -> ORIGINAL VALUE
        self.reverse_mapping = {}

        # Counter for each entity type
        self.counters = defaultdict(int)

    def get_placeholder(
        self,
        entity_type: str,
        value: str,
    ) -> str:
        """
        Return the same placeholder for repeated values.
        """

        key = (
            entity_type,
            value.lower(),
        )

        if key in self.forward_mapping:
            return self.forward_mapping[key]

        self.counters[entity_type] += 1

        placeholder = (
            f"[{entity_type}_{self.counters[entity_type]:03d}]"
        )

        self.forward_mapping[key] = placeholder
        self.reverse_mapping[placeholder] = value

        return placeholder

    def get_original_value(
        self,
        placeholder: str,
    ):
        """
        Return original value from placeholder.
        """

        return self.reverse_mapping.get(placeholder)

    def get_all_mappings(self):
        """
        Return all placeholder mappings.
        """

        return self.reverse_mapping