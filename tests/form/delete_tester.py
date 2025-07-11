from abc import abstractmethod
from typing import Optional, Set, Tuple, Union

from conftest import TitledUrlRepr
from django.db.models import Model, QuerySet
from django.forms import Form
from django.http import HttpResponse
from form.base_form_tester import (
    AnonymousSubmitTester,
    AuthorisedSubmitTester,
    SubmitTester,
    UnauthorizedSubmitTester,
)
from form.base_tester import BaseTester


class DeleteTester(BaseTester):
    @property
    @abstractmethod
    def unauthenticated_user_error(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def anonymous_user_error(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def successful_delete_error(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def only_one_delete_error(self):
        raise NotImplementedError

    @abstractmethod
    def status_error_message(self, by_user: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def redirect_error_message(
        self, by_user: str, redirect_to_page: Union[TitledUrlRepr, str]
    ):
        raise NotImplementedError

    def get_redirect_to_page_repr(self, redirect_to_page):
        if isinstance(redirect_to_page, str):
            redirect_to_page_repr = redirect_to_page
        elif isinstance(redirect_to_page, tuple):  # expected TitledUrlRepr
            (
                redirect_pattern,
                redirect_repr,
            ), redirect_title = redirect_to_page
            redirect_to_page_repr = f"{redirect_title} ({redirect_repr})"
        else:
            raise AssertionError(
                f"Unexpected value type `{type(redirect_to_page)}` "
                "for `redirect_to_page`"
            )
        return redirect_to_page_repr

    def test_delete_item(
        self, qs: QuerySet, delete_url_addr: str, only_base_form: bool = False
    ) -> HttpResponse:
        instances_before: Set[Model] = set(qs.all())

        can_delete, response = self.user_can_delete(
            UnauthorizedSubmitTester(tester=self, test_response_cbk=None),
            delete_url_addr,
            self._item_adapter,
            qs=qs,
        )
        assert not can_delete, self.unauthenticated_user_error

        can_delete, response = self.user_can_delete(
            AnonymousSubmitTester(tester=self, test_response_cbk=None),
            delete_url_addr,
            self._item_adapter,
            qs=qs,
        )
        assert not can_delete, self.anonymous_user_error

        can_delete, response = self.user_can_delete(
            AuthorisedSubmitTester(
                tester=self,
                test_response_cbk=(
                    AuthorisedSubmitTester.get_test_response_ok_cbk(tester=self)
                ),
            ),
            delete_url_addr,
            self._item_adapter,
            qs=qs,
            only_base_form=only_base_form,
        )
        assert can_delete, self.successful_delete_error

        instances_after: Set[Model] = set(qs.all())

        deleted_instances_n = instances_before - instances_after
        assert len(deleted_instances_n) == 1, self.only_one_delete_error

        return response

    def user_can_delete(
        self,
        submitter: SubmitTester,
        delete_url,
        item_to_delete_adapter,
        qs: QuerySet,
        only_base_form: bool = False,
    ) -> Tuple[Optional[bool], Optional[HttpResponse]]:
        if only_base_form:
            try:
                get_response = submitter.client.get(delete_url)
            except Exception as error:
                raise AssertionError(
                    "При обработке GET-запроса автора комментария к странице "
                    "удаления комментария возникло исключение: "
                    f"{error}"
                )
            if "form" in get_response.context:
                assert isinstance(get_response.context["form"], Form), (
                    "Убедитесь, что на страницу удаления комментария не "
                    "передается форма, которая используются для создания "
                    "комментария. При использовании класса `DeleteVeiw` из "
                    "модуля `django.views.generic` для реализации view-класса "
                    "для удаления комментариев не задавайте значение атрибута "
                    "класса `form_class`."
                )
        response = submitter.test_submit(url=delete_url, data={})
        deleted = qs.filter(id=item_to_delete_adapter.id).first() is None
        return deleted, response
