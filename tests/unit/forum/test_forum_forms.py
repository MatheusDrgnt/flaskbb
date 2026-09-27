"""
Tests for the forum forms (validation).

Includes a parametrized test (Tarefa 1.4).

The tests depend on the ``database`` fixture because flaskbb resolves
validation error messages through flask_babelplus, which queries the
``settings`` table for the configured default language.

Note: NewTopicForm requires a non-empty title, but does not impose
minimum or maximum length constraints; that is why the "too short"
and "too long" cases are still considered valid at the field level.
"""

import pytest

from flaskbb.forum.forms import NewTopicForm, ReportForm, SearchPageForm


# ---------------------------------------------------------------------------
# NewTopicForm — parametrized (Tarefa 1.4)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "title,content,title_ok,content_ok",
    [
        ("Valid topic title here", "Content long enough to pass.", True, True),
        ("", "Content long enough to pass.", False, True),
        ("ab", "Content long enough to pass.", True, True),
        ("Valid title", "", True, False),
        ("x" * 300, "Content long enough to pass.", True, True),
    ],
)
def test_new_topic_form_field_validation_matrix(
    application, database, default_settings,
    title, content, title_ok, content_ok
):
    """Parametrized: NewTopicForm field validation across 5 combinations.

    Covers valid input (happy path) and invalid inputs at the field
    level (empty title, empty content).
    """
    with application.test_request_context():
        form = NewTopicForm(title=title, content=content)
        form.title.validate(form)
        form.content.validate(form)

        assert (form.title.errors == []) is title_ok
        assert (form.content.errors == []) is content_ok


# ---------------------------------------------------------------------------
# ReportForm
# ---------------------------------------------------------------------------


def test_report_form_accepts_valid_reason(application, database, default_settings):
    """Happy path: ReportForm reason accepts a non-empty value."""
    with application.test_request_context():
        form = ReportForm(reason="This post violates the rules.")
        form.reason.validate(form)
        assert form.reason.errors == []


def test_report_form_rejects_empty_reason(application, database, default_settings):
    """Error: ReportForm reason rejects an empty value."""
    with application.test_request_context():
        form = ReportForm(reason="")
        form.reason.validate(form)
        assert form.reason.errors != []


# ---------------------------------------------------------------------------
# SearchPageForm
# ---------------------------------------------------------------------------


def test_search_page_form_rejects_empty_query(application, database, default_settings):
    """Error: SearchPageForm query rejects an empty value."""
    with application.test_request_context():
        form = SearchPageForm(search_query="")
        form.search_query.validate(form)
        assert form.search_query.errors != []


def test_search_page_form_accepts_valid_query(application, database, default_settings):
    """Happy path: SearchPageForm query accepts a valid value."""
    with application.test_request_context():
        form = SearchPageForm(search_query="flask")
        form.search_query.validate(form)
        assert form.search_query.errors == []