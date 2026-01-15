class EmailAddress:

    def __init__(self, address: str):
        normalized = self.normalize_address(address)
        if not self._check_correct_email(normalized):
            raise ValueError(f"Invalid email address: {address}")
        self._address = normalized

    @property
    def address(self) -> str:
        return self._address

    @property
    def masked(self) -> str:
        name, domain = self._address.split("@")
        return f"{name[:2]}**@{domain}"

    def normalize_address(self, value: str) -> str:

        return value.strip().lower()

    def _check_correct_email(self, value: str) -> bool:

        if "@" not in value:
            return False
        if not (
            value.endswith(".com") or value.endswith(".ru") or value.endswith(".net")
        ):
            return False

        return True
