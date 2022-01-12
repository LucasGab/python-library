from typing import List


class Book:
    def __init__(self,name: str,publisher: str,author: str,is_issued: bool,id: int = -1) -> None:
        self.__id = id
        self.__name = name
        self.__publisher = publisher
        self.__author = author
        self.__is_issued = is_issued


    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self,name:str):
        self.__name = name

    @property
    def publisher(self) -> str:
        return self.__publisher

    @publisher.setter
    def publisher(self,publisher:str):
        self.__publisher = publisher

    @property
    def author(self) -> str:
        return self.__author

    @author.setter
    def author(self,author:str):
        self.__author = author 
    
    @property
    def is_issued(self) -> bool:
        return self.__is_issued