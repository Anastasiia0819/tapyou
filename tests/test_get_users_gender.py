import requests
import allure
from config.settings import Config

@allure.suite("API вакансий")
@allure.sub_suite("GET /users?gender=")
class TestGetUsersGender:
    @allure.feature("Запрос пользователей по гендеру")
    @allure.title("Успешный запрос списка id пользователей с параметром male")
    def test_get_users_male(self):
        gender = "male"
        headers = {"accept": "application/json"}
        response_get_users_male = requests.get(Config.get_user_by_gender(gender), headers=headers)
        with allure.step("Проверка статус-кода"):
            assert response_get_users_male.status_code == 200
        with allure.step("Проверка структуры ответа"):
            response_get_users_male_json = response_get_users_male.json()
            assert response_get_users_male_json["isSuccess"] is True
            assert "idList" in response_get_users_male_json
            assert isinstance(response_get_users_male_json.get("idList"), list)
            assert len(response_get_users_male_json["idList"]) > 0
        with allure.step("Проверка наличия id пользователя из БД"):
            assert 10 in response_get_users_male_json['idList']  # Значение ID из ответа (на проекте данные берем из БД)

    @allure.feature("Запрос пользователей по гендеру")
    @allure.title("Успешный запрос списка id пользователей с параметром female")
    def test_get_users_male(self):
        gender = "female"
        headers = {"accept": "application/json"}
        response_get_users_female = requests.get(Config.get_user_by_gender(gender), headers=headers)
        with allure.step("Проверка статус-кода"):
            assert response_get_users_female.status_code == 200
        with allure.step("Проверка структуры ответа"):
            response_get_users_female_json = response_get_users_female.json()
            assert response_get_users_female_json["isSuccess"] is True
            assert "idList" in response_get_users_female_json
            assert isinstance(response_get_users_female_json.get("idList"), list)
            assert len(response_get_users_female_json["idList"]) > 0
        with allure.step("Проверка наличия id пользователя из БД"):
            assert 5 in response_get_users_female_json['idList']  # Значение ID из ответа (на проекте данные берем из БД)

    @allure.feature("Запрос пользователей по гендеру")
    @allure.title("Проверка обязательности параметра gender")
    def test_test_get_users_without_gender(self):
        gender = None
        headers = {"accept": "application/json"}
        response_get_users_without_gender = requests.get(Config.get_user_by_gender(gender), headers=headers)
        response_get_users_without_gender_json = response_get_users_without_gender.json()
        assert response_get_users_without_gender.status_code == 400
        assert response_get_users_without_gender_json["errorMessage"] == "Required String parameter 'gender' is not present"

    @allure.feature("Запрос пользователей по гендеру")
    @allure.title("Запрос списка пользователей с невалидным значением параметра gender")
    def test_get_users_invalid_gender(self):
        gender = "test"
        headers = {"accept": "application/json"}
        with allure.step(f"Запрос с невалидным значением параметра gender: {gender}"):
            response_get_users_invalid_gender = requests.get(Config.get_user_by_gender(gender), headers=headers)
        with allure.step("Проверка статус-кода"):
            assert response_get_users_invalid_gender.status_code == 404
        with allure.step(f"Проверка ошибки для gender={gender}"):
            response_get_users_invalid_gender_json = response_get_users_invalid_gender.json()
            assert response_get_users_invalid_gender_json['isSuccess'] is False
            assert response_get_users_invalid_gender_json['errorCode'] == 404
            assert response_get_users_invalid_gender_json['errorMessage'] == "not found" #добавить актуальный errorMessage после обновления спецификации












