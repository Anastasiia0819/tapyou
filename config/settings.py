class Config:
    base_url = f"https://hr-challenge.dev.tapyou.com/api/test"
    headers = {"accept": "application/json"}

    @staticmethod
    def get_user_by_id(user_id):
        return f"{Config.base_url}/user/{user_id}"

    @staticmethod
    def get_user_by_gender(gender):
        return f"{Config.base_url}/users?gender={gender}"

    @staticmethod
    def get_headers():
        return Config.headers

