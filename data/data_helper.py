import random
import string


class DataHelper:
    @staticmethod
    def generate_random_string(length=10):
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    
    @staticmethod
    def generate_email():
        return f"test_{DataHelper.generate_random_string(10)}@example.com"
    
    @staticmethod
    def generate_password():
        return DataHelper.generate_random_string(10)
    
    @staticmethod
    def generate_name():
        return f"TestUser_{DataHelper.generate_random_string(8)}"
