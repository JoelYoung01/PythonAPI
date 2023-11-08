"""Utility functions for the app."""


def get_updated_value(old_value: str, new_value: str) -> str:
    """Compares two strings.
    Returns the new value if it is not "null", "none", or "".
    Returns the old value if the new value is None.
    Returns None if the new value is "null", "none", or "".

    Args:
        old_value (str): The old value.
        new_value (str): The new value.

    Returns:
        str: The updated value.
    """
    if new_value is not None and new_value.lower() in ["null", "none", ""]:
        return None

    return new_value or old_value
