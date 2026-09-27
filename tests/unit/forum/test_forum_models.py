"""
Tests for the forum domain models.

These tests exercise the business behaviour of the forum app
(Category, Forum, Topic) at the unit level. They are stable,
run fast, and do not depend on the permission system.
"""

import pytest

from flaskbb.forum.models import Category, Forum, Topic


# ---------------------------------------------------------------------------
# Category
# ---------------------------------------------------------------------------


def test_category_is_persisted(database, category):
    """Happy path: a saved category can be retrieved by id."""
    found = Category.get_by(id=category.id)
    assert found is not None
    assert found.title == "Test Category"


def test_category_lookup_with_unknown_id_returns_none(database):
    """Error: querying an unknown category id returns None."""
    found = Category.get_by(id=99999)
    assert found is None


def test_category_delete_removes_it(database, category):
    """Happy path: deleting a category removes it from the DB."""
    category_id = category.id
    category.delete()
    assert Category.get_by(id=category_id) is None


def test_category_has_forums_relationship(database, category, forum):
    """Border: a category with a forum exposes it via get_forums."""
    forums = category.forums
    assert forum in forums


# ---------------------------------------------------------------------------
# Forum
# ---------------------------------------------------------------------------


def test_forum_is_persisted(database, forum):
    """Happy path: a saved forum can be retrieved by id."""
    found = Forum.get_by(id=forum.id)
    assert found is not None
    assert found.title == "Test Forum"


def test_forum_lookup_with_unknown_id_returns_none(database):
    """Error: querying an unknown forum id returns None."""
    found = Forum.get_by(id=99999)
    assert found is None


def test_forum_slug_is_url_safe(database, forum):
    """Border: forum title is slugified for URLs."""
    assert forum.slug
    assert " " not in forum.slug


def test_forum_belongs_to_category(database, forum, category):
    """Happy path: a forum references its parent category."""
    assert forum.category_id == category.id


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------


def test_topic_is_persisted(database, topic):
    """Happy path: a saved topic can be retrieved by id."""
    found = Topic.get_by(id=topic.id)
    assert found is not None
    assert found.title == "Test Topic Normal"


def test_topic_lookup_with_unknown_id_returns_none(database):
    """Error: querying an unknown topic id returns None."""
    found = Topic.get_by(id=99999)
    assert found is None


def test_topic_starts_with_zero_views(database, topic):
    """Border: a freshly created topic starts with 0 views."""
    found = Topic.get_by(id=topic.id)
    assert found.views == 0


def test_topic_belongs_to_forum(database, topic, forum):
    """Happy path: a topic references its parent forum."""
    assert topic.forum_id == forum.id


def test_topic_has_slug(database, topic):
    """Border: a topic exposes a URL-safe slug."""
    assert topic.slug
    assert " " not in topic.slug