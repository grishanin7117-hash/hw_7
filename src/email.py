from dataclasses import dataclass, field, replace
from typing import Optional, Union, List
from src.utils import clean_text
from src.email_address import EmailAddress
from src.status import Status


@dataclass
class Email:
    subject: str
    body: str
    sender: EmailAddress
    recipients: Union[EmailAddress, List[EmailAddress]]
    status: Status = Status.DRAFT
    date: Optional[str] = None
    short_body: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.recipients, EmailAddress):
            self.recipients = [self.recipients]

    def get_recipients_str(self) -> str:
        return ", ".join(r.address for r in self.recipients)

    def clean_data(self) -> "Email":
        self.subject = clean_text(self.subject)
        self.body = clean_text(self.body)
        return self

    def add_short_body(self, n: int = 10) -> "Email":
        if not self.body:
            self.short_body = None
            return self
        if len(self.body) <= n:
            self.short_body = self.body
        else:
            self.short_body = self.body[:n] + "..."
        return self

    def is_valid_fields(self) -> bool:
        return bool(self.subject and self.body)

    def prepare(self) -> "Email":
        self.clean_data()
        if not self.sender or not self.recipients or not self.is_valid_fields():
            self.status = Status.INVALID
        else:
            self.status = Status.READY
        return self

    def __str__(self) -> str:
        recipients_str = self.get_recipients_str()
        return (
            f"Status: {self.status}\n"
            f"Кому: {recipients_str}\n"
            f"От: {self.sender.masked}\n"
            f"Тема: {self.subject}, дата {self.date}\n"
            f"{self.short_body or self.body}"
        )

    def __repr__(self):
        return (
            f"Email(От: {self.sender.address}, "
            f"Кому: {[r.address for r in self.recipients]}, "
            f"Тема: {self.subject}, "
            f"Статус: {self.status.value})"
        )
