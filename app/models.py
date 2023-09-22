import re


class User:
    def __init__(self, user_id, first_name, last_name, phone, email, score=0):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.score = score

    @staticmethod
    def is_valid_email(email):
        return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email)

    @staticmethod
    def is_valid_phone(phone):
        return re.fullmatch(
            r"^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$",
            phone,
        )
