from datetime import datetime
from typing import List
from src.email import Email
from src.status import Status


class EmailService:

    def __init__(self, email: Email):
        self.email = email

    def add_send_date(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")

    def send_email(self) -> List[Email]:
        results = []
        # если список получателей пуст
        if not self.email.recipients:
            return []

        for recipient in self.email.recipients:
            sent = Email(
                subject=self.email.subject,
                body=self.email.body,
                sender=self.email.sender,
                recipients=[recipient],
                status=self.email.status,
            )
            sent.date = self.add_send_date()
            if self.email.status == Status.READY:
                sent.status = Status.SENT
            else:
                sent.status = Status.FAILED
            results.append(sent)
        return results


class LoggingEmailService(EmailService):

    def send_email(self) -> List[Email]:

        results = super().send_email()
        with open("send.log", "a", encoding="utf-8") as f:
            for email in results:
                f.write(
                    f"[{email.date}] {email.status} -> {email.get_recipients_str()}\n"
                )
        return results
