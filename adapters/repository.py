from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

import config
from domain.model import CopiedMessage, ProxyChat
from sqlalchemy.orm import Session


class AbstractRepository(ABC):

    @abstractmethod
    def list_all_copied_messages(self) -> List[CopiedMessage]:
        raise NotImplementedError

    @abstractmethod
    def find_copied_message(self, copied_message_id: int) -> Optional[CopiedMessage]:
        raise NotImplementedError

    @abstractmethod
    def find_copied_message_by_origin_id(self, origin_message_id: int) -> Optional[CopiedMessage]:
        raise NotImplementedError

    @abstractmethod
    def add_copied_message(
        self, 
        origin_chat_id: int, 
        origin_message_id: int, 
        copied_message_id: int
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_all_proxychats(self) -> List[ProxyChat]:
        raise NotImplementedError

    @abstractmethod
    def find_proxychat(self, chat_id: int) -> Optional[ProxyChat]:
        raise NotImplementedError

    @abstractmethod
    def add_proxychat(self, chat_id: int, name: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def set_proxychat_listening(self, chat_id: int, listening: bool) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_proxychat_name(self, chat_id: int, name: str) -> None:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def list_all_copied_messages(self) -> List[CopiedMessage]:
        copied_messages = self.session.query(CopiedMessage).all()
        self.session.expunge_all()
        return copied_messages

    def find_copied_message(self, copied_message_id: int) -> Optional[CopiedMessage]:
        copied_message = self.session.query(CopiedMessage).filter_by(copied_message_id=copied_message_id).first()
        self.session.expunge_all()
        return copied_message

    def find_copied_message_by_origin_id(self, origin_message_id: int) -> Optional[CopiedMessage]:
        copied_message = self.session.query(CopiedMessage).filter_by(origin_message_id=origin_message_id).first()
        self.session.expunge_all()
        return copied_message
    
    def add_copied_message(
        self, 
        origin_chat_id: int, 
        origin_message_id: int, 
        copied_message_id: int
    ) -> None:
        if self.find_copied_message(copied_message_id) is not None:
            return

        copied_message = CopiedMessage(
            origin_chat_id=origin_chat_id, 
            origin_message_id=origin_message_id, 
            copied_message_id=copied_message_id
            )
        self.session.add(copied_message)

    def list_all_proxychats(self) -> List[ProxyChat]:
        copied_messages = self.session.query(ProxyChat).all()
        self.session.expunge_all()
        return copied_messages

    def find_proxychat(self, chat_id: int) -> Optional[ProxyChat]:
        proxy_chat = self.session.query(ProxyChat).filter_by(chat_id=chat_id).first()
        self.session.expunge_all()
        return proxy_chat

    def add_proxychat(self, chat_id: int, name: str) -> bool:
        if self.find_proxychat(chat_id=chat_id) is not None:
            return False

        proxy_chat = ProxyChat(chat_id=chat_id, name=name, listening=True)
        self.session.add(proxy_chat)
        return True

    def set_proxychat_listening(self, chat_id: int, listening: bool) -> None:
        proxy_chat = self.session.query(ProxyChat).filter_by(chat_id=chat_id).first()
        if proxy_chat is None:
            return

        proxy_chat.listening = listening
        self.session.add(proxy_chat)

    def set_proxychat_name(self, chat_id: int, name: str) -> None:
        proxy_chat = self.session.query(ProxyChat).filter_by(chat_id=chat_id).first()
        if proxy_chat is None:
            return

        proxy_chat.name = name
        self.session.add(proxy_chat)
        