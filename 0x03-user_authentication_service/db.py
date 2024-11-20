#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User, Base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class DB:
    """DB class to manage the SQLite database.

    This class handles the initialization of the database and provides
    methods for interacting with the database, such as adding users.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance."""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session: Session | None = None

    @property
    def _session(self) -> Session:
        """Memoized session object.

        This property initializes the session only once and returns
        it for further database operations.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database.

        Args:
            email (str): The user's email address.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user in the database using arbitrary keyword arguments.

        Args:
            **kwargs: The filtering criteria for finding the user.

        Raises:
            NoResultFound: If no results are found for the provided criteria.
            InvalidRequestError: If the provided arguments are invalid.

        Returns:
            User: The first User object matching the criteria.
        """
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No user found matching the criteria.")
        except Exception as e:
            raise InvalidRequestError("Invalid query parameters provided.")\
                from e

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes in the database.

        Args:
            user_id (int): The ID of the user to be updated.
            **kwargs: The user's attributes to update.

        Raises:
            NoResultFound: If no user is found with the provided user_id.
            ValueError: If an invalid attribute is provided for update.
        """
        user = self.find_user_by(id=user_id)

        valid_attributes = {attr.name for attr in User.__table__.columns}

        for key, value in kwargs.items():
            if key not in valid_attributes:
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)

        self._session.commit()
