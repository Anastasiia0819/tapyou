import requests
import allure
from config.settings import Config
import pytest

@allure.suite("API вакансий")
@allure.sub_suite("GET /users?gender=")
class TestGetUsersGender:
    @allure.feature("Запрос пользователей по гендеру")
    @allure.title("Успешный запрос списка id пользователей с параметрами female/male")
    @pytest.mark.parametrize("gender, expected_ids", [("male", [10, 20]), ("female", [5, 15])])
    def test_get_users_genders(self,gender,expected_ids):
        headers = Config.get_headers()
        response_get_users_genders = requests.get(Config.get_user_by_gender(gender), headers=headers)
        with allure.step("Проверка статус-кода"):
            assert response_get_users_genders.status_code == 200
        with allure.step("Проверка структуры ответа"):
            response_get_users_genders_json = response_get_users_genders.json()
            assert response_get_users_genders_json["isSuccess"] is True
            assert "idList" in response_get_users_genders_json
            assert isinstance(response_get_users_genders_json.get("idList"), list)
            assert len(response_get_users_genders_json["idList"]) > 0
        with allure.step("Проверка наличия id пользователя из БД"):
            # Значение ID из ответа (на проекте данные берем из БД)
            for expected_id in expected_ids:
                assert expected_id in response_get_users_genders_json['idList']

    @allure.feature("Запрос пользователей по гендеру")
    @allure.title("Проверка обязательности параметра gender")
    def test_test_get_users_without_gender(self):
        gender = None
        headers = Config.get_headers()
        response_get_users_without_gender = requests.get(Config.get_user_by_gender(gender), headers=headers)
        response_get_users_without_gender_json = response_get_users_without_gender.json()
        assert response_get_users_without_gender.status_code == 400
        assert response_get_users_without_gender_json["errorMessage"] == "Required String parameter 'gender' is not present"

    @allure.feature("Запрос пользователей по гендеру")
    @allure.title("Запрос списка пользователей с невалидным значением параметра gender")
    @pytest.mark.parametrize("invalid_gender, expected_error_code, expected_error_message",
                             [("test_gender", 404, "not found gender"),
                              ("1male", 400, "NumberFormatException: For input string: \"1male\"")])
    def test_get_users_invalid_gender(self, invalid_gender, expected_error_code, expected_error_message):
        headers = Config.get_headers()
        with allure.step(f"Запрос с невалидным значением параметра gender: {invalid_gender}"):
            response_get_users_invalid_gender = requests.get(Config.get_user_by_gender(invalid_gender), headers=headers)
        with allure.step("Проверка статус-кода"):
            assert response_get_users_invalid_gender.status_code == expected_error_code
        with allure.step(f"Проверка ошибки для gender={invalid_gender}"):
            response_get_users_invalid_gender_json = response_get_users_invalid_gender.json()
            assert response_get_users_invalid_gender_json['isSuccess'] is False
            assert response_get_users_invalid_gender_json['errorCode'] == expected_error_code
            assert response_get_users_invalid_gender_json['errorMessage'] == expected_error_message #добавить актуальный errorMessage









