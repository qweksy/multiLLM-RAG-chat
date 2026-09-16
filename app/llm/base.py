from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """
    Абстракция над генерацией текста LLM. Все роутеры и сервисы работают только с этим интерфейсом.
    Конкретный провайдер (LLM модель) подставляется через fabric.py и никогда не импортируется вне её.
    """
    
    @abstractmethod
    def gen_anwer(self, prompt: str) -> str:
        """Отправляет промпт в модель и возвращает строковый ответ."""
        
        raise NotImplementedError
    
class EmbeddingProvider(ABC):
    """
    Абстракция над вычислением эмбеддингов. Намеренно отделена от LLMProvider.
    Не каждый провайдер генерации текста умеет считать эмбеддинги.
    Конкретный провайдер (модель для эмбеддингов) подставляется через fabric.py и никогда не импортируется вне её.
    """
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Идентификатор модели эмбеддингов. Сохраняется в documents.embedding_model"""
        
        raise NotImplementedError
    
    @abstractmethod
    def embed_text(self, text: str) -> list[float]:
        """Векторизует один текст, используется для запроса пользователя"""
        
        raise NotImplementedError
    
    @abstractmethod
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Векторизует список всех текстов за один вызов."""
        
        raise NotImplementedError