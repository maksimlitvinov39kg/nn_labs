import streamlit as st

def run_streamlit_app(generator, config):
    
    if st.button("Инициализировать модель"):
        st.success("Модель успешно загружена!")

        gen_params = config["generation_params"]
        prompt = st.text_area("Введите текст для продолжения", "Александр Сергеевич Пушкин родился в ")

        # Создаем слайдеры и чекбоксы для всех параметров генерации
        max_length = st.slider("Максимальная длина текста", 
                              min_value=20, 
                              max_value=500, 
                              value=gen_params["max_length"])
        
        min_length = st.slider("Минимальная длина текста", 
                              min_value=10, 
                              max_value=max_length, 
                              value=gen_params["min_length"])
        
        num_return_sequences = st.slider("Количество вариантов текста", 
                                       min_value=1, 
                                       max_value=5, 
                                       value=gen_params["num_return_sequences"])
        
        temperature = st.slider("Температура", 
                              min_value=0.1, 
                              max_value=2.0, 
                              value=gen_params["temperature"], 
                              step=0.1)
        
        top_k = st.slider("Top-K", 
                          min_value=1, 
                          max_value=100, 
                          value=gen_params["top_k"])
        
        top_p = st.slider("Top-P", 
                          min_value=0.0, 
                          max_value=1.0, 
                          value=gen_params["top_p"], 
                          step=0.1)
        
        repetition_penalty = st.slider("Штраф за повторения", 
                                     min_value=1.0, 
                                     max_value=2.0, 
                                     value=gen_params["repetition_penalty"], 
                                     step=0.1)
        
        length_penalty = st.slider("Штраф за длину", 
                                 min_value=0.1, 
                                 max_value=2.0, 
                                 value=gen_params["length_penalty"], 
                                 step=0.1)
        
        no_repeat_ngram_size = st.slider("Размер N-грамм без повторений", 
                                        min_value=1, 
                                        max_value=5, 
                                        value=gen_params["no_repeat_ngram_size"])
        
        do_sample = st.checkbox("Использовать сэмплинг", 
                               value=gen_params["do_sample"])
        
        early_stopping = st.checkbox("Ранняя остановка", 
                                   value=gen_params["early_stopping"])

        # Опциональные поля для префикса и суффикса
        use_prefix = st.checkbox("Использовать префикс")
        if use_prefix:
            prefix = st.text_input("Префикс", value=gen_params["prefix"])
        else:
            prefix = ""

        use_suffix = st.checkbox("Использовать суффикс")
        if use_suffix:
            suffix = st.text_input("Суффикс", value=gen_params["suffix"])
        else:
            suffix = ""

        if st.button("Сгенерировать текст"):
            if prompt.strip() == "":
                st.error("Пожалуйста, введите текст для генерации.")
            else:
                # Добавляем префикс и суффикс к промпту
                full_prompt = f"{prefix}{prompt}{suffix}"
                
                # Собираем все параметры генерации в словарь
                generation_params = {
                    "max_length": max_length,
                    "min_length": min_length,
                    "num_return_sequences": num_return_sequences,
                    "do_sample": do_sample,
                    "temperature": temperature,
                    "top_k": top_k,
                    "top_p": top_p,
                    "repetition_penalty": repetition_penalty,
                    "length_penalty": length_penalty,
                    "no_repeat_ngram_size": no_repeat_ngram_size,
                    "early_stopping": early_stopping
                }

                # Генерируем текст
                generated_texts = generator.generate_text(
                    prompt=full_prompt,
                    **generation_params
                )

                # Выводим все сгенерированные варианты
                st.subheader("Сгенерированные варианты:")
                for i, text in enumerate(generated_texts, 1):
                    st.write(f"Вариант {i}:")
                    st.write(text)
                    st.write("---")

if __name__ == "__main__":
    st.error("Этот файл нужно запускать через main.py")