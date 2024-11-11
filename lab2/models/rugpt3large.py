from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

class RUGPT3Large:
    def __init__(self, model_name_or_path, device='auto'):
        """
        Инициализация модели и токенизатора.

        :param model_name_or_path: Название модели или путь к модели.
        :param device: Устройство для выполнения (по умолчанию 'auto' для выбора между 'cuda' и 'cpu').
        """
        self.device = device if device != 'auto' else ('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
        self.model = GPT2LMHeadModel.from_pretrained(model_name_or_path).to(self.device)

    def generate_text(
        self,
        prompt,
        max_length=50,
        min_length=10,
        num_return_sequences=1,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.8,
        repetition_penalty=1.2,
        length_penalty=1.0,
        no_repeat_ngram_size=3,
        early_stopping=True
    ):
        """
        Генерация текста на основе входного промпта.

        :param prompt: Исходный текстовый промпт для генерации
        :param max_length: Максимальная длина сгенерированного текста
        :param min_length: Минимальная длина сгенерированного текста
        :param num_return_sequences: Количество вариантов сгенерированного текста
        :param do_sample: Использовать ли сэмплинг при генерации
        :param temperature: Параметр температуры для управления креативностью
        :param top_k: Количество токенов с наибольшей вероятностью для выбора
        :param top_p: Порог накопленной вероятности для выбора токенов
        :param repetition_penalty: Штраф за повторение токенов
        :param length_penalty: Штраф за длину генерируемого текста
        :param no_repeat_ngram_size: Размер n-грамм, которые не должны повторяться
        :param early_stopping: Остановка генерации при достижении условий
        :return: Список сгенерированных текстов
        """
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        
        outputs = self.model.generate(
            input_ids=input_ids,
            max_length=max_length,
            min_length=min_length,
                        sequences= num_return_sequences,
            do_sample=do_sample,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            length_penalty=length_penalty,
            no_repeat_ngram_size=no_repeat_ngram_size,
            early_stopping=early_stopping
        )
        
        generated_texts = []
        for output in outputs:
            generated_texts.append(self.tokenizer.decode(output, skip_special_tokens=True))
        
        return generated_texts
