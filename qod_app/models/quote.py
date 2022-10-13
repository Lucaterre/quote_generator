# -*- coding: UTF-8 -*-

"""
quote.py

Model declaration for Quote used in database
"""

from ..extensions import db


class Quote(db.Model):
    """Quote model"""
    __tablename__ = "quotes"
    # define a searchable field for msearch extension
    __searchable__ = ['quote']
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quote = db.Column(db.String(100), default="")
    author = db.Column(db.String(100), default="")
    source = db.Column(db.String(100), default="unknown")
    category = db.Column(db.String(100), default="others")

    @property
    def serialize(self):
        """this property serialize a user object into a dict
        object"""
        return {
         "quote_id": self.id,
         "quote": self.quote,
         "author": self.author,
         "source": self.source,
         "category": self.category,
        }

    @staticmethod
    def get_all_quotes(limit_threshold: int = None) -> list:
        """Returns all quotes or a limited number quotes

        :param limit_threshold: limit number of results
        :type: int
        :return: list of quotes
        :rtype: list
        """
        # control size of limit_threshold to control overflow SQL integer exception
        try:
            return [quote.serialize for quote in Quote.query.limit(limit_threshold).all()]
        except OverflowError:
            return [quote.serialize for quote in Quote.query.all()]

    @staticmethod
    def get_unique_authors() -> list:
        """return a list of all distinct authors

        :return: list of authors available
        :rtype: list
        """
        return [author[0] for author in db.session.query(Quote.author).distinct().all()]

    @staticmethod
    def get_unique_categories() -> list:
        """return a list of all distinct categories

        :return: list of categories available
        :rtype: list
        """
        return [category[0] for category in db.session.query(Quote.category).distinct().all()]

    @staticmethod
    def get_unique_sources() -> list:
        """return a list of all distinct sources

        :return: list of sources available
        :rtype: list
        """
        return [source[0] for source in db.session.query(Quote.source).distinct().all()]

    @staticmethod
    def updated_quote(new_values: dict) -> dict:
        """this method updated values of a quote with its ID from a Quote model

        :param new_values: a dict that contains values to update a quote
        :type: dict
        :return: a quote updated and serialized
        :rtype: dict
        """
        quote_to_updated = Quote.query.filter(Quote.id == new_values['quote_id']).first()
        quote_history = quote_to_updated.serialize
        quote_to_updated.quote = new_values['quote']
        quote_to_updated.author = new_values['author']
        quote_to_updated.source = new_values['source']
        quote_to_updated.category =new_values['category']
        db.session.commit()
        return quote_history

    @staticmethod
    def delete_quote(quote_id: int) -> dict:
        """this method delete a quote with its ID from a Quote Model

        :param quote_id: id of quote
        :type: int
        :return: a quote deleted and serialized
        :rtype: dict
        """
        quote_to_remove = Quote.query.filter(Quote.id == quote_id).first()
        quote_history = quote_to_remove.serialize
        db.session.delete(quote_to_remove)
        db.session.commit()
        return quote_history
