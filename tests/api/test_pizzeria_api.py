import pytest
import allure
from utils.api_helper import APIHelper
from utils.logger import logger
from config import Config

@allure.suite("API Tests")
@allure.feature("Public API")
class TestPizzeriaAPI:
    
    @pytest.fixture(scope="class")
    def api(self):
        """Fixture to provide an APIHelper instance."""
        return APIHelper()

    @allure.title("Проверка доступности API (список страниц)")
    def test_get_pages_api(self, api: APIHelper):
        response = api.get("pages")
        
        with allure.step("Проверить код ответа 200"):
            assert response.status_code == 200
            
        with allure.step("Проверить, что в ответе есть список страниц"):
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0

    @allure.title("Проверка получения конкретной страницы (Главная)")
    def test_get_home_page_api(self, api: APIHelper):
        page_id = "150"
        response = api.get(f"pages/{page_id}")
            
        if response.status_code == 200:
            with allure.step("Проверить заголовок страницы"):
                assert "Пиццерия" in response.json()['title']['rendered']
        else:
            pytest.skip(f"Страница с ID {page_id} не найдена на этом стенде")
