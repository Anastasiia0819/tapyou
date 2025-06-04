import requests
import pytest
import allure
from config.settings import Config
import time

@allure.suite("API вакансий")
@allure.sub_suite("GET /user/{id}")
class TestGetUserId:
    @allure.feature("Запрос пользователя по id")
    @allure.title("Получение информации о пользователе при вводе в поле id валидного значения")
    @pytest.mark.parametrize("gender", ["male", "female"])
    def test_get_user_id_from_user_list(self,gender):
        with allure.step("Получаем id пользователей из запроса users?gender=male"):
            headers = Config.get_headers()
            response_user_id_from_gender = requests.get(Config.get_user_by_gender(gender), headers=headers)
            user_ids = response_user_id_from_gender.json()["idList"]

        with allure.step("Запрос инфо о пользователе по id"):
            for user_id in user_ids:
                response_user_id_info = requests.get(Config.get_user_by_id(user_id), headers=headers)
                assert response_user_id_info.status_code == 200
                response_user_id_info_json = response_user_id_info.json()
                assert response_user_id_info_json["isSuccess"] is True
                assert "user" in response_user_id_info_json
                user = response_user_id_info_json["user"]
                assert user["id"] == user_id
                assert isinstance(user['id'], int)
                #для проверки корректности полученного пользователя, можно брать знаечния для проверки из БД
                assert "name" in user and user["name"]is not None
                assert 'gender' in user and user["gender"] is not None
                # проверка, что все пользователи с корректным гендером
                assert user["gender"] == gender
                assert 'age' in user and isinstance(user['age'], int)
                assert 'city' in user and user["city"] is not None
                assert 'registrationDate' in user and user["registrationDate"] is not None

    @allure.feature("Запрос пользователя по id")
    @allure.title("Получение информации о пользователе при вводе в поле id невалидного значения")
    @pytest.mark.parametrize("invalid_id, expected_error_code, expected_error_message",
                             [(-1, 404, "not found"),
                              (0, 404, "not found"),
                              ("1q", 400, "NumberFormatException: For input string: \"1q\""),
                              ("!", 400, "NumberFormatException: For input string: \"!\"")])
    def test_get_user_info_invalid_id(self, invalid_id,expected_error_code,expected_error_message):
        headers = Config.get_headers()
        response_invalid_id = requests.get(Config.get_user_by_id(invalid_id), headers=headers)
        assert response_invalid_id.status_code == expected_error_code
        response_invalid_id_json = response_invalid_id.json()
        assert response_invalid_id_json["isSuccess"] is False
        assert response_invalid_id_json["errorCode"] == expected_error_code
        assert response_invalid_id_json["errorMessage"] == expected_error_message
        assert response_invalid_id_json["user"] is None


    @allure.feature("Запрос пользователя по id")
    @allure.title("Проверка обязательности параметра id")
    def test_get_user_info_without_id(self):
        user_id = None
        headers = Config.get_headers()
        url_without_user_id = f"{Config.base_url}/user/"
        response_without_id = requests.get(url_without_user_id, headers=headers)
        assert response_without_id.status_code == 400
        response_without_id_json = response_without_id.json()
        assert response_without_id_json["errorCode"] == 400
        assert response_without_id_json["errorMessage"] == "Required String parameter 'id' is not present"

    @allure.feature("Запрос пользователя по id")
    @allure.title("Проверка значения параметра id, которого нет в базе")
    def test_get_user_not_found(self):
        with allure.step("Получаем id пользователей из запроса users?gender=male и users?gender=female"):
            headers = Config.get_headers()
            gender_1 = "male"
            gender_2 = "female"
            response_user_id_from_gender_male = requests.get(Config.get_user_by_gender(gender_1), headers=headers)
            response_user_id_from_gender_female = requests.get(Config.get_user_by_gender(gender_2), headers=headers)
            response_user_id_male_json = response_user_id_from_gender_male.json()
            response_user_id_female_json = response_user_id_from_gender_female.json()
            ## Объединение двух списков id в один
            user_ids_male = response_user_id_male_json["idList"]
            user_ids_female = response_user_id_female_json["idList"]
            all_user_ids = user_ids_male + user_ids_female

        with allure.step("Проверка ошибки, если id не присутствует в списке пользователей"):
            invalid_id = max(all_user_ids) + 1
            assert invalid_id not in all_user_ids
            response_id_not_user = requests.get(Config.get_user_by_id(invalid_id), headers=headers)
            with allure.step(f"Проверка ответа для невалидного ID {invalid_id}"):
                assert response_id_not_user.status_code == 404

            response_id_not_user_json = response_id_not_user.json()
            assert response_id_not_user_json["isSuccess"] == False
            assert response_id_not_user_json["errorCode"] == 404
            assert response_id_not_user_json["errorMessage"] == "not found"
            assert response_id_not_user_json["user"] is None

    @allure.feature("Запрос пользователя по id")
    @allure.title("Проверка производительности при загрузке информации о пользователе")
    @pytest.mark.parametrize("gender", ["male", "female"])
    def test_performance_for_get_user_info_by_id(self, gender):
        headers = Config.get_headers()
        with allure.step(f"Запрос с параметром gender={gender}"):
            response_get_users = requests.get(Config.get_user_by_gender(gender), headers=headers)
            response_get_users_json = response_get_users.json()
            # Cписок пользователей (ID)
            user_ids = response_get_users_json["idList"]
            even_ids = [user_id for user_id in user_ids if user_id % 2 == 0]  # четное id
            odd_ids = [user_id for user_id in user_ids if user_id % 2 != 0]  # нечетное id

            # Выбираем первый четный и первый нечетный id
            even_id = even_ids[0] if len(even_ids) > 0 else None
            odd_id = odd_ids[0] if len(odd_ids) > 0 else None

            if even_id:
                with allure.step(f"Запрос на получение данных для четного id {even_id}"):
                    start_time = time.time()  # Начало измерения времени
                    response_even_id = requests.get(Config.get_user_by_id(even_id), headers=headers)
                    elapsed_time_even = time.time() - start_time  # Вычисление времени отклика
                    print(f"Time for even ID ({even_id}): {elapsed_time_even} seconds")
                    assert response_even_id.status_code == 200

            if odd_id:
                with allure.step(f"Запрос на получение данных для нечетного id {odd_id}"):
                    start_time = time.time()  # Начало измерения времени
                    response_odd_id = requests.get(Config.get_user_by_id(odd_id), headers=headers)
                    elapsed_time_odd = time.time() - start_time  # Вычисление времени отклика
                    print(f"Time for odd ID ({odd_id}): {elapsed_time_odd} seconds")
                    assert response_odd_id.status_code == 200

            # Проверка, что разница во времени отклика между четным и нечетным id не превышает порог
            max_allowed_diff = 0.1  # в секундах

            if even_id and odd_id:
                time_diff = abs(elapsed_time_even - elapsed_time_odd)
                assert time_diff <= max_allowed_diff, f"Time difference between even and odd ID requests is too high: {time_diff} seconds"














