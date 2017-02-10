from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from .views import *


class IndexTest(TestCase):
    def test_access_to_index_page(self):
        """
        Access to the index page
        """
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "trash/index.html")


class AddItemTest(TestCase):
    fixtures = ['init_data.json']

    def test_access_to_add_item_page(self):
        """
        Access to the add item page, should return a list of bins
        """
        response = self.client.get(reverse("additem"))
        self.assertIsNotNone(response.context["bins"])

    def test_item_successfully(self):
        """
        Add item, should redirect to index page after success
        """
        args = {
            "name": "Name",
            "description": "Description",
            "bin": "Paper",
            "sc_code": 123
        }
        response = self.client.post(reverse("additem"), args)
        self.assertTrue(ADD_ITEM_SUCCESSFULLY_MESSAGE in response.cookies['messages'].value)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, "/auction/")


class TrashBinsTest(TestCase):
    fixtures = ['init_data.json']

    def test_access_to_trash_bins_page(self):
        """
        Access to the trash bins page
        """
        response = self.client.get(reverse("trashbins"))
        self.assertTemplateUsed(response, "trash/bins.html")

    def test_show_bin_items_with_not_existing_bin(self):
        """
        Show items of the not existing bin, should redirect to main page
        """
        bin_name = "money"
        response = self.client.get(reverse("show_binitems", args=(bin_name,)))
        self.assertRedirects(response, "/")

    def test_show_bin_items_with_existing_bin(self):
        """
        Show items of the existing bin
        """
        bin_name = "plastic"
        response = self.client.get(reverse("show_binitems", args=(bin_name,)))
        self.assertContains(response, b"plastic")
        self.assertTemplateUsed(response, "trash/binitems.html")


class SearchTest(TestCase):
    fixtures = ['init_data.json']

    def test_search_not_existing_bar_code(self):
        """
        Search not existing bar code, should redirect to main page
        """
        context = {
            "criteria": NOT_FOUND_BAR_CODE
        }
        response = self.client.get(reverse("search"), context)
        self.assertRedirects(response, "/")

    def test_search_all(self):
        """
        Search all items, return list of items and redirect to search result page
        """
        context = {
            "criteria": ""
        }
        response = self.client.get(reverse("search"), context)
        self.assertTrue(len(response.context["items"]) <= 20)
        self.assertIsNotNone(response.context["items"])
        self.assertTemplateUsed(response, "trash/searchresult.html")

    def test_search_by_name(self):
        """
        Search for specific items by name, return match list of items
        """
        context = {
            "criteria": "spoon"
        }
        response = self.client.get(reverse("search"), context)
        self.assertIsNotNone(response.context["items"])
        self.assertTrue("spoon" in response.context["items"][0].name)

    def test_search_by_code_existing_items(self):
        """
        Search for existing items by code, return match list of items
        """
        context = {
            "criteria": "scnr12345"
        }
        response = self.client.get(reverse("search"), context)
        self.assertIsNotNone(response.context["items"])
        self.assertTrue("12345" in response.context["items"][0].sc_code)

    def test_search_by_code_not_existing_items(self):
        """
        Search for not existing items by code, redirect to the add item page
        """
        new_sc_code = "9999"
        context = {
            "criteria": "scnr" + new_sc_code
        }
        response = self.client.get(reverse("search"), context)
        self.assertRedirects(response, "/additem/?scnf={}".format(new_sc_code))


class MapTest(TestCase):
    def test_open_map(self):
        response = self.client.get(reverse("openmap"))
        self.assertIsNotNone(response.context["data"])
        self.assertTemplateUsed(response, "trash/maps.html")


class AboutUsTest(TestCase):
    def test_access_about_page(self):
        response = self.client.get(reverse("aboutus"))
        self.assertTemplateUsed(response, "trash/aboutus.html")